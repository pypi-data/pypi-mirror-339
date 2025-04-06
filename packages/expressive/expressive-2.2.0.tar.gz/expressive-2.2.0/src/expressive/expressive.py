#!/usr/bin/env python3

""" Copyright 2024-2025 Russell Fordyce

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import re
import threading
import time
import warnings
from html import escape as html_escape
from textwrap import dedent as text_dedent
from textwrap import indent as text_indent

import numba
import numpy
import sympy
from sympy.utilities.lambdify import MODULES as lambdify_modules

from .version import version as __version__  # noqa F401

DTYPES_SUPPORTED = {
    # numpy.dtype("bool"):     1,
    numpy.dtype("uint8"):    8,
    numpy.dtype("uint16"):  16,
    numpy.dtype("uint32"):  32,
    numpy.dtype("uint64"):  64,
    numpy.dtype("int8"):     8,
    numpy.dtype("int16"):   16,
    numpy.dtype("int32"):   32,
    numpy.dtype("int64"):   64,
    numpy.dtype("float32"): 32,
    numpy.dtype("float64"): 64,
    # numpy.dtype("float128"): 128,  # not supported in Numba [ISSUE 65]
    numpy.dtype("complex64"):   64,
    numpy.dtype("complex128"): 128,
    # numpy.dtype("complex256"): 256,
}

NS10E9 = 10**9  # factor for nanoseconds to second(s)

# SymPy floating-point Atoms
SYMPY_ATOMS_FP = (
    # straightforward floats
    sympy.Float,
    # trancendental constants
    sympy.pi,
    sympy.E,
    # FUTURE general scipy.constants support
    # common floating-point functions
    sympy.log,
    sympy.exp,
    # sympy.sqrt,  # NOTE simplifies to Pow(..., Rational(1,2))
    # sympy.cbrt,  #   can be found with expr.match(cbrt(Wild('a')))
    # trig functions
    sympy.sin, sympy.asin, sympy.sinh, sympy.asinh,
    sympy.cos, sympy.acos, sympy.cosh, sympy.acosh,
    sympy.tan, sympy.atan, sympy.tanh, sympy.atanh,
    sympy.cot, sympy.acot, sympy.coth, sympy.acoth,
    sympy.sec, sympy.asec, sympy.sech, sympy.asech,
    sympy.csc, sympy.acsc, sympy.csch, sympy.acsch,
    sympy.sinc,
    sympy.atan2,
    # LambertW?  # FUTURE results in float or complex result [ISSUE 107]
)

# FIXME this is an unstable API for now which might change between versions
#   in the future, this should have a deprecation system which can at a minimum
#   warn or error about older config settings which have been migrated, in addition
#   to continuing support until some known version
# TODO additionally fixing some schema is critical for a good config system
# TODO config value to delete inherited keys/trees and use the default (which may be absent or None)
CONFIG = {
    "warnings": {},  # TODO keep other sections or centralize?
    "translate_simplify": {  # FUTURE consider splitting
        "parse": {},  # coerce ^ -> ** Pow() warning?
        "build": {
            # attempt to reduce `Sum()` instances
            "sum": {
                # `Sum() is expressly an unevaluated summation
                # set to False to prevent this path, which first tries summation and may do other
                # simplifications on the inner function, always converting to a dedicated
                # function which loops over the given range, which may have symbolic (start,end)
                #
                # many `Sum()` instances can be converted to expressions, potentially avoiding a loop
                # of unknown length, such as here (where the range is not known in advance)
                #   >>> parse_expr("Sum(x, (x, a, b))").replace(Sum,summation)
                #  -a**2/2 + a/2 + b**2/2 + b/2
                # `Sum()` can always be replaced by `summation()`, which may produce a simpler expression
                # or the same or a simpler `Sum()` instance
                "try_algebraic_convert": True,
                # warn users after N seconds if sum() simplification is taking an excessive amount of time
                # set the value
                #  - to some positive integer for a timeout in seconds
                #  - False to disable this and never spawn a thread
                #
                # as this spawns a new Thread, some users who are careful about their thread count
                # or are using some model that clashes with them may want to disable this
                # users can also simplify their `Sum()`s before passing them in
                # similarly, Windows users may find Thread generally problematic and wish to disable this
                # TODO this feels like it would be happier in a warnings meta-section
                # TODO this may make sense as part of a general simplifications thread or process
                #   (processes can be killed and benefit from `fork()`)
                "threaded_timeout_warn": 20,  # seconds, yes this is a huge default
            }
        },
    },
    # "data": {},  # some data choices probably makes sense
    "backend": {
        "numba": {  # others?
            # "fastmath": True,
            # "parallel": True,
            # needs for like distributing cached files on a network share?.. [ISSUE 24]
        },
    },
}


# helpers for warnings
class ExpressiveWarning(RuntimeWarning):
    pass


def warn(msg):
    warnings.warn(msg, ExpressiveWarning)


def data_cleanup(data):
    """ verify the incoming data can be used

        currently this expects a dict of numpy arrays

        FUTURE optional other numpy-backed arrays support (ie. Pandas, Polars, etc.)
          for now, users can use the relevant .to_numpy() methods
          also consider .to_records()
    """
    if not data:
        raise ValueError("no data provided")
    if not isinstance(data, dict):
        raise TypeError(f"data must be a dict of NumPy arrays or scalars, but got {type(data)}")

    data_cleaned = {}
    vector_length = {}
    for name, ref in data.items():
        # check name is sensible
        # NOTE that expr parsing removes spaces, which might mash symbols together
        if not isinstance(name, str):
            raise ValueError(f"data names must be strings, but got {type(name)}: {repr(name)}")
        # NOTE `name.isidentifier()` and "\w+" allow some unsuitable valies like "π" and "_"
        if not name.isidentifier() or name.startswith("_") or name.endswith("_") or not re.match(r"^[a-zA-Z\d_]+$", name):
            raise ValueError(f"data names must be valid Python names (identifiers) and Symbols, but got '{name}'")
        # TODO consider warning for keywords `keyword.iskeyword(name)`, but allow some?.. like "del"
        # coerce single python values to 0-dim numpy values
        if isinstance(ref, (int, float, complex)):
            # NOTE chooses widest, signed type for Python values (int64,float64,complex128)
            #   if users want another type, just choose it (ie. `numpy.uint32(10)`)
            # TODO is there a better way to do automatic typing?
            # TODO config option to prefer min type `numpy.array(ref, numpy.min_scalar_type(ref))`
            ref = numpy.array(ref)[()]
        if not isinstance(ref, (numpy.ndarray, numpy.number)):
            raise TypeError(f"data must be a dict of NumPy arrays or scalars, but has member ({name}:{type(ref)})")
        if ref.dtype not in DTYPES_SUPPORTED:
            raise TypeError(f"unsupported dtype ({name}:{ref.dtype})")
        # NOTE single (ndim==0) values have shape==() and `len(array)` raises `TypeError: len() of unsized object`
        if ref.ndim == 0:
            vector_length[name] = 0
        elif ref.ndim == 1:
            vector_length[name] = len(ref)
        else:
            vector_length[name] = len(ref)  # FUTURE further analysis needed for additional dimensions
        data_cleaned[name] = ref

    # compare shapes and warn for mixed dimensions
    shapes = set(ref.shape for ref in data_cleaned.values()) - {()}  # ignore single values (0-dim)
    if len(shapes) > 1 and any(ref.ndim > 1 for ref in data.values()):
        warn(f"mixed dimensions may not broadcast correctly, got shapes={shapes}")

    # FUTURE consider support for uneven input arrays when indexed [ISSUE 10]
    #   specifically offsets can make it so the data does not need the same lengths or
    #   can be padded to be the correct length automatically
    #   however, this also seems ripe for confusion and errors
    vector_lengths = set(vector_length.values())
    if vector_lengths == {0}:
        raise ValueError("only single values passed (ndim=0), no arrays (at least a result array must be passed to determine length)")
    elif len(vector_lengths - {0}) != 1:
        raise ValueError(f"uneven data lengths (must be all equal or 0 (non-vector)): {vector_lengths}")

    return data_cleaned


def symbols_given_cleanup(expr, symbols):
    """ helper for producing a mapping of names to symbols
        if unsure or only partially available, prefer to return less over guessing
        this lets a user pass only what the need and let Expressive figure out
        the rest

        FUTURE make some use of SymPy Assumptions (.assumptions0)
          https://docs.sympy.org/latest/guides/assumptions.html
          https://docs.sympy.org/latest/modules/core.html#sympy.core.basic.Basic.assumptions0
    """
    # all are extracted from expr post-parsing if no Symbols are passed (probably None)
    if not symbols:
        return {}

    types_supported_symbols = (sympy.Symbol, sympy.IndexedBase, sympy.Idx)

    if isinstance(symbols, types_supported_symbols):  # singular Symbol as argument
        return {symbols.name: symbols}

    if isinstance(symbols, (list, tuple, set)):
        for symbol in symbols:
            if not isinstance(symbol, types_supported_symbols):
                raise TypeError(f"symbols must be a collection of SymPy Symbols, but got {type(symbol)}")
        return {s.name: s for s in symbols}

    if isinstance(symbols, dict):
        for name, symbol in symbols.items():
            if not isinstance(name, str):
                raise TypeError(f"all names must be strings (str), but got {type(name)}: {name}")
            if not isinstance(symbol, types_supported_symbols):
                raise TypeError(f"unsupported Symbol {type(symbol)}: {symbol}, expected {types_supported_symbols}")
            if symbol.name != name:
                warn(f"name '{name}' doesn't match symbol.name '{symbol.name}' ({sympy.srepr(symbol)})")
        return symbols

    raise TypeError(f"expected a collection of SymPy Symbols, but got ({type(symbols)})")


def dummy_symbols_split(expr, symbols):
    """ extract names that are exclusively used as dummy variables
        for example in `Sum(x, (x, 1, y))`, `x` is not needed or used from data
        and replaced by some function of `y`

        only symbols which are exclusively a dummy will be split out
    """
    dummy_symbols = {}

    # collect dummy values from `Sum()` limits
    # TODO move verification to an earlier step in Expressive.__init__()
    for sum_block in expr.atoms(sympy.Sum):
        if expr.atoms(sympy.Indexed):
            raise NotImplementedError(f"mixing indexing and Sum is not (yet) supported: {expr.atoms(sympy.Indexed)}")
        fn_sum = sum_block.function
        limits = sum_block.limits  # tuple of tuples
        # easy validity checks
        if len(limits) != 1:
            raise NotImplementedError(f"only exactly 1 Sum() limits is supported for now: {limits}")
        if fn_sum.atoms(sympy.Sum):
            raise NotImplementedError(f"nested Sum instances not yet supported: {sum_block} wraps {fn_sum}")
        # entire expr is checked for IndexedBase for now
        # if fn_sum.atoms(sympy.Indexed):  # TODO consider walrus operator and including IndexedBase
        #     raise NotImplementedError(f"indexed Sum are not yet supported: {sum_block} -> {fn_sum.atoms(sympy.Indexed)}")

        # separate and compare limit features
        dummy_var, limit_start, limit_stop = limits[0]
        if not isinstance(limit_start, (sympy.Symbol, sympy.Integer)):
            raise TypeError(f"unsupported type for limit start '{limit_start}': {type(limit_start)}")
        if not isinstance(limit_stop, (sympy.Symbol, sympy.Integer)):
            raise TypeError(f"unsupported type for limit stop '{limit_stop}': {type(limit_stop)}")
        if isinstance(limit_start, sympy.Integer) and isinstance(limit_stop, sympy.Integer):
            if limit_start > limit_stop:  # TODO consider support for negative sum range (`{Sum((_,a,b)):-Sum((_,b,a))}`?)
                raise ValueError(f"fixed Sum() limits start({limit_start}) > stop({limit_stop}) represents a zero or negative range")
            # if limit_start == limit_stop:  # FUTURE simplifier can directly convert this to fn_sum (all fixed limits?)
            #     warn(f"fixed Sum() limits start({limit_start}),stop({limit_stop}) can be eliminated")

        # keep a collection of all dummy_symbols
        # TODO can this use `dummy_symbols_split()` result? (mostly avoiding KeyError from data[dummy])
        dummy_symbols[dummy_var.name] = dummy_var

    # remove dummy symbols from args collection
    # NOTE symbols collection is mutated here (by-ref) in addition to being returned
    for name in dummy_symbols.keys():
        try:
            del symbols[name]
        except KeyError as ex:  # pragma nocover impossible/bug path
            raise RuntimeError(f"BUG: dummy var '{name}' missing during split from symbols collection: {repr(ex)}")

    return symbols, dummy_symbols


def string_expr_cleanup(expr_string):
    """ a few rounds of basic cleanup to ease usage
        equality is transformed to Eq() form
            `LHS = RHS` -> `LHS==RHS` -> `Eq(LHS,RHS)`
    """
    # FUTURE consider if these can or should use the SynPy transformation system
    #   https://docs.sympy.org/latest/modules/parsing.html#parsing-transformations-reference
    if not isinstance(expr_string, str):
        raise ValueError("expr must be a string")

    if "<" in expr_string or ">" in expr_string:
        raise ValueError("inequality is not supported")

    # discard all whitespace to ease string processing
    # this will make (invalid) collections like "a b c" into "abc", not "a*b*c"
    # as a user might conceivably expect, though this does not claim to ..but
    # if so this will be later highlighted when the data is not valid as no
    # "abc" symbol name exists in the given data unless some very special
    # circumstance arises
    # TODO raise or warn for mashing names together [ISSUE 101]
    #   "a cos(b)" -> "acos(b)"
    expr_string = re.sub(r"\s+", r"", expr_string)  # expr_string.replace(" ", "")

    # coerce runs of "=" into exactly "=="
    # ideally only (0,1,2) exist, but let users be really excited ==== for now
    expr_string = re.sub(r"=+", "==", expr_string)
    count_equalities = expr_string.count("=") // 2
    if count_equalities == 1:
        lhs, rhs = expr_string.split("==")  # ValueError if doesn't unpack exactly
        # recurse for each half, then rejoin 'em
        lhs = string_expr_cleanup(lhs)
        rhs = string_expr_cleanup(rhs)
        return f"Eq({lhs}, {rhs})"
    elif count_equalities > 1:  # not exactly 0 or 1 (==)
        raise SyntaxError(f"only 1 equivalence (==) can be provided, but parsed {count_equalities}: {expr_string}")

    # user probably meant Pow() not bitwise XOR
    # TODO add to warning subsystem `if "^" in expr_string:`
    # TODO allow configuring this warning too [ISSUE 29]
    expr_string = expr_string.replace("^", "**")

    # multiplication cleanup blocks
    # SymPy expects symbols to be separated from Numbers for multiplication
    #   ie. "5x+7" -> "5*x+7"
    # however, care needs to be taken to avoid splitting symbols and functions
    # which contain a number, like `t3`, `log2()`, etc.

    # clean up the case where trailing number isn't multiplied like it should be
    #   ie. "(a+b)2" -> "(a+b)*2"
    # TODO add to warning subsystem as it feels like an unusual style [ISSUE 29]
    #   and could easily be a typo like missing Pow '^' or other operator which
    #   would otherwise be silently "fixed"
    # NOTE SymPy might handle this case without the additional '*' after 1.12
    expr_string = re.sub(r"(\))(\d+)", r"\1*\2", expr_string)

    # consider matches where a number appears directly after
    #   start of string | basic operators "+-*/" | open parenthesis
    # and directly before a case where
    #   new string starts (symbol or function)
    #   new parentheses block starts "3(a+b)" -> "3*(a+b)"
    # likely this could be better tokenized by Python AST or SymPy itself
    expr_string = re.sub(r"(^|[\+\-\*\/]|\()(\d+)([a-zA-Z]|\()", r"\1\2*\3", expr_string)

    # make sure there's something left after parsing
    #  (ie. user didn't just pass " " or something went badly ary above)
    if not expr_string:
        raise ValueError("no content after cleanup")

    return expr_string


def get_or_create_symbol(dict_search, name, symbol_cls):
    """ helper like `dict.get(name, sym(name))` which checks matches are the expected type
        this is useful specifically to ensure passed Symbols are more specific types
            IndexedBase
            Idx
        otherwise they can't be used later
    """
    try:
        value = dict_search[name]
    except KeyError:
        return symbol_cls(name)  # directly make one from the name
    if not isinstance(value, symbol_cls):  # name in dict, but wrong type!
        raise TypeError(f"{name} should be type {symbol_cls}, but got {type(value)}")
    return value


def string_expr_indexing_offsets(expr_string, symbols):
    """ detect and manage relative offsets
        returns tuple with
         - offset values like `symbols` mapping {name:Symbol}
         - range the index can be (inclusive)
        symbols will be used if they have the same name as discovered values
        raising if the name is the same, but the Symbol type is wrong
        (refer to get_or_create_symbol)

        for example, given
            a[i+1] + b[i-1]
        this returns like
            offset_values {
                "a": IndexedBase("a")
                "b": IndexedBase("b")
                "i": Idx("i")
            }
            offset_ranges {
                Idx("i"): [-1, 1],
            }
    """
    # FUTURE handle advanced relative indexing logic [ISSUE 11]
    # FUTURE consider if multiple Idx can generate deeper loops
    offset_values = {}
    offset_ranges = {}  # spread amongst offsets as name:[min,max]
    for chunk in re.findall(r"(\w+)\[(.+?)\]", expr_string):
        base, indexing_block = chunk
        indexer = str(sympy.parse_expr(indexing_block).free_symbols.pop())
        try:  # extract the offset amount ie. x[i-1] is -1
            offset = sympy.parse_expr(indexing_block).atoms(sympy.Number).pop()
        except KeyError:
            offset = 0  # no offset like x[i]
        offset_values[base]    = get_or_create_symbol(symbols, base, sympy.IndexedBase)
        offset_values[indexer] = get_or_create_symbol(symbols, indexer, sympy.Idx)
        # now update the spread for the offset
        indexer = offset_values[indexer]  # use Idx ref directly, not name
        spread = offset_ranges.get(indexer, [0, 0])  # start fresh if missing
        spread[0] = min(spread[0], offset)
        spread[1] = max(spread[1], offset)
        offset_ranges[indexer] = spread  # creates if new

    # really make sure there is exactly zero or one indexing Symbols Idx
    if len(offset_ranges) > 1:
        raise ValueError(f"only a single Idx is supported, but got: {offset_ranges}")

    return offset_values, offset_ranges


def indexed_offsets_from_expr(expr):
    """ parse indexed offset features from a SymPy expr

        parallels `string_expr_indexing_offsets()`, though this expects
        the caller to ensure any symbols are present in expr before calling
    """
    if not isinstance(expr, (sympy.core.expr.Expr, sympy.core.relational.Equality)):
        raise RuntimeError(f"BUG: expected SymPy Expr or Equality, but got {type(expr)}")

    offset_values = {}
    offset_ranges = {}  # spread amongst offsets as name:[min,max]
    for block in expr.atoms(sympy.Indexed):
        base    = block.atoms(sympy.IndexedBase)
        indexer = block.atoms(sympy.Idx)
        if len(base) != 1:  # FIXME is this possible?
            raise ValueError(f"multiple or nested IndexedBase: {block}")
        if len(indexer) != 1:
            raise ValueError(f"indexer must be a single Idx, but got {block}")
        base    = base.pop()  # exactly 1 value exists
        indexer = indexer.pop()
        # now calculate the offset
        offset = (block.atoms(sympy.Rational, sympy.Float) or {0})  # ideally Integer or empytset{}->{0}
        if offset != (block.atoms(sympy.Integer) or {0}):  # error for fractional indicies
            raise ValueError(f"expected a single Integer (or nothing: 0) as the offset, but parsed {block}")
        offset_values[base]    = base
        offset_values[indexer] = indexer
        offset = offset.pop()  # {N} -> N
        spread = offset_ranges.get(indexer, [0, 0])  # start fresh if missing (alt. defaultdict(lambda))
        spread[0] = min(spread[0], offset)
        spread[1] = max(spread[1], offset)
        offset_ranges[indexer] = spread  # creates entry if this is the first instance

    if len(offset_ranges) > 1:
        raise ValueError(f"only a single Idx is supported, but got: {offset_ranges}")

    return offset_values, offset_ranges


def string_expr_to_sympy(expr_string, name_result=None, symbols=None):
    """ parse string to a SymPy expression
        this is largely support logic to help sympy.parse_expr()
         - support for indexing Symbols via IndexBase[Idx]
         - helps make symbol reference collections consistent before and after parsing
           ie. `reference in e.atoms(IndexedBase)` or `foo is atom` are True

        note that `parse_expr()` creates new symbols for any un-named values

        collections of Symbols are returned as dicts mapping {name:Symbol},
        even if there is only a single Symbol
        while any indexer (Idx) is returned as a mapping of
          {Idx:[low index,high index]}
        so the templated loop won't over or under-run its array indices

        FUTURE work with transformation system over regex hackery where possible
    """
    if symbols is None:
        symbols = {}

    # collection of {name:Symbol} mappings for `sympy.parse_expr()`
    local_dict = symbols

    # get indexing Symbols (IndexedBase, Idx) and the spread of any indexer(s)
    #   members of symbols will be used if they're the correct type, otherwise
    #   TypeError will be raised for names which exist, but are not valid for
    #   their respective types (see `get_or_create_symbol()`)
    # NOTE for now there can only be exactly 1 or 0 indexers (Idx) (for now?)
    offset_values, offset_ranges = string_expr_indexing_offsets(expr_string, symbols)

    # continue to build up symbols dict for `sympy.parse_expr()`
    local_dict.update(offset_values)

    # convert forms like `expr_rhs` into `Eq(result_lhs, expr_rhs)`
    verify_literal_result_symbol = False  # avoid NameError in later check
    if not expr_string.startswith("Eq("):
        if "=" in expr_string:
            raise RuntimeError(f"BUG: failed to handle equality during cleanup: {expr_string}")
        if name_result is None:
            verify_literal_result_symbol = True  # enable later warning path checks
            name_result = "result"
        # rewrite `expr_string` to `Eq()` form
        if offset_values:
            syms_result = get_or_create_symbol(symbols, name_result, sympy.IndexedBase)
            # FUTURE reconsider if supporting multiple indexers
            # unpack name (rather than smuggling it from the earlier loop..)
            indexer = next(iter(offset_ranges))
            expr_string = f"Eq({syms_result.name}[{indexer.name}], {expr_string})"
        else:
            syms_result = get_or_create_symbol(symbols, name_result, sympy.Symbol)
            expr_string = f"Eq({syms_result.name}, {expr_string})"
        # pack result into locals before parse
        local_dict.update({name_result: syms_result})

    expr_sympy = sympy.parse_expr(expr_string, local_dict=local_dict)

    if not expr_sympy.atoms(sympy.Eq):  # ensures (lhs,rhs) properties, alt: hasattr
        raise RuntimeError(f"BUG: didn't coerce into Eq(LHS, RHS) form: {expr_sympy}")

    # now (re-)extract the result Symbol from LHS
    # NOTE IndexedBase coerced to Symbol [ISSUE 9]
    atoms_lhs = expr_sympy.lhs.atoms(sympy.Symbol)
    # FUTURE opportunity to extract Number from LHS to fail or divide out
    if len(atoms_lhs) == 1:
        pass  # pop later, set of exactly 1 Symbol
    elif len(atoms_lhs) == 2:
        atoms_lhs = expr_sympy.lhs.atoms(sympy.IndexedBase)
        if len(atoms_lhs) != 1:
            raise ValueError(f"multiple possible result values: {atoms_lhs}")
    else:
        raise ValueError(f"multiple or no possible result values from LHS atoms:{atoms_lhs}")
    symbol_result = atoms_lhs.pop()  # now dissolve set: {x} -> x

    if name_result is not None and name_result != symbol_result.name:
        raise ValueError(f"mismatch between name_result ({name_result}) and parsed symbol name ({symbol_result.name})")

    # make dicts of {name:Symbol} for caller
    # NOTE `symbol_result` must be last to simplify dropping via slicing in later logic
    # NOTE `.atoms(Symbol)` picks up IndexedBase, but demotes them to new `Symbol` instances [ISSUE 9]

    # warn the user if they passed unused symbols
    names_unused = set(symbols.keys()) - {s.name for s in expr_sympy.atoms(sympy.Symbol)}
    if names_unused:  # set logic
        warn(f"some symbols were not used: {names_unused}")

    symbols = {s.name: s for s in expr_sympy.atoms(sympy.Symbol)}
    symbols.update({s.name: s for s in expr_sympy.atoms(sympy.IndexedBase)})
    symbols.pop(symbol_result.name)  # restored later as the last entry
    for indexer in offset_ranges.keys():  # expressly remove Idx name(s)
        del symbols[indexer.name]

    # force lexical ordering by-name for consistency (becomes args, etc.)
    symbols = {name: symbols[name] for name in sorted(symbols.keys())}

    # make a dict (len==1) of the result symbol
    syms_result = {symbol_result.name: symbol_result}
    # now append it to the symbols dict so it can be an argument
    symbols.update(syms_result)  # always the last symbol

    # hint that user may be misusing "result" name in their RHS
    if verify_literal_result_symbol and (
        name_result in {a.name for a in expr_sympy.rhs.atoms(sympy.Symbol)}) and (
        name_result not in offset_values.keys()
    ):
        warn("symbol 'result' in RHS refers to result array, but not indexed or passed as name_result")

    return expr_sympy, symbols, offset_ranges, syms_result


def parse_sympy_expr(expr, name_result, symbols):
    """ get a compatible set of objects for later use, mirroring `string_expr_to_sympy()`,
        but for a valid SymPy expr (may be an Expr or Equality)
            expr           SymPy expr
            symbols        {s:s.name}             sorted, no indexer, result last
            offset_ranges  {indexer:[min,max]}    indexer is Idx
            result         {result:resultsymbol}  always a dict of len 1
    """
    if symbols:  # NOTE rewritten later from expr
        symbols_unused = set(symbols.values()) - expr.atoms(sympy.Symbol, sympy.IndexedBase, sympy.Idx)
        if symbols_unused:
            raise ValueError(f"some symbols not present in expr: {symbols_unused}")

    offset_values, offset_ranges = indexed_offsets_from_expr(expr)

    if expr.atoms(sympy.Eq):  # form Eq(LHS,RHS) TODO consider `isinstance(e,Equality)` instead
        if len(expr.atoms(sympy.Eq)) != 1:
            raise ValueError(f"only a single equality can exist, but got {expr.atoms(sympy.Eq)}")
        result = (expr.lhs.atoms(sympy.IndexedBase) or expr.lhs.atoms(sympy.Symbol))
        if len(result) != 1:  # `indexed_offsets_from_expr()` ensures only a single value exists
            raise ValueError(f"BUG: expected a single result, but got {expr.lhs}")
        result = result.pop()
        if name_result is not None and result.name != name_result:
            raise ValueError(f"mismatched name between name_result({name_result}) and LHS({result})")
    else:  # form RHS -> Eq(result,RHS)
        # NOTE because all symbols exist, user can't pass "result" naively
        if name_result is None:
            name_result = "result"
            if "result" in (a.name for a in expr.atoms(sympy.Symbol, sympy.IndexedBase, sympy.Idx)):
                warn("symbol 'result' in RHS refers to result array, but not indexed or passed as name_result")
        if expr.atoms(sympy.IndexedBase):  # RHS reveals indexing
            indexer = next(iter(offset_ranges))
            result  = get_or_create_symbol(symbols, name_result, sympy.IndexedBase)
            expr    = sympy.Eq(result[indexer], expr)
        else:
            result  = get_or_create_symbol(symbols, name_result, sympy.Symbol)
            expr    = sympy.Eq(result, expr)

    symbols = {s.name: s for s in expr.atoms(sympy.Symbol)}
    symbols.update({s.name: s for s in expr.atoms(sympy.IndexedBase)})
    symbols.pop(result.name)  # restored later as the last entry
    for indexer in offset_ranges.keys():  # expressly remove Idx name(s)
        del symbols[indexer.name]

    # force lexical ordering by-name for consistency (becomes args, etc.)
    symbols = {name: symbols[name] for name in sorted(symbols.keys())}

    # make a dict (len==1) of the result symbol
    result_dict = {result.name: result}
    # now append it to the symbols dict so it can be an argument
    symbols.update(result_dict)  # always the last symbol

    return expr, symbols, offset_ranges, result_dict


def dtype_result_guess(expr, data):
    """ attempt to automatically determine the resulting dtype given an expr and data

        this is a backup where the user has not provided a result dtype
        possibly it could support warning for likely wrong dtype

        this is not expected to be a general solution as the problem is open-ended
        and likely depends on the real data

        WARNING this logic assumes the highest bit-width is 64
          larger widths will require rewriting some logic!
          intermediately a user should specify the type, assuming
          a (future) numba really has support for it

        FUTURE consider  `numpy.dtype.alignment`
    """
    # set of dtypes from given data
    dtypes_expr = {c.dtype for c in data.values()}  # set of NumPy types

    # throw out some obviously bad cases
    if not dtypes_expr:
        raise ValueError("no data provided")
    dtypes_unsupported = dtypes_expr - set(DTYPES_SUPPORTED.keys())
    if dtypes_unsupported:
        raise TypeError(f"unsupported dtypes: {dtypes_unsupported}")

    # always return a complex type if present
    if numpy.dtype("complex128") in dtypes_expr or expr.atoms(sympy.I):
        return numpy.dtype("complex128")
    # complex64 is a pair of 32-bit floats, but some types don't cast nicely
    if numpy.dtype("complex64") in dtypes_expr:
        width_noncomplex = max(DTYPES_SUPPORTED[dt] for dt in dtypes_expr if not dt.kind == "c")
        if not width_noncomplex or width_noncomplex <= 32:
            return numpy.dtype("complex64")
        if numpy.dtype("int64") in dtypes_expr or numpy.dtype("uint64") in dtypes_expr:
            warn(f"cast complex inputs to complex128 to avoid loss of precision with 64-bit ints ({dtypes_expr})")
            return numpy.dtype("complex64")
        if numpy.dtype("float64") not in dtypes_expr:
            raise RuntimeError(f"BUG: expected float64, but got {dtypes_expr}")
        return numpy.dtype("complex128")

    max_bitwidth = max(DTYPES_SUPPORTED[dt] for dt in dtypes_expr)

    # FUTURE support for float128 (does Numba support this?)
    if max_bitwidth > 64:
        raise RuntimeError(f"BUG: max_bitwidth {max_bitwidth}: only complex types exceeding 64 are supported: {dtypes_expr}")

    # now only
    if numpy.dtype("float64") in dtypes_expr:
        return numpy.dtype("float64")
    # promote 32-bit float to 64-bit when greater types are present
    if numpy.dtype("float32") in dtypes_expr:
        if max_bitwidth > 32:
            return numpy.dtype("float64")
        return numpy.dtype("float32")

    # detect structures that make the result logically floating-point
    # TODO perhaps these should be part of a structured attempt to constrain inputs
    #   in addition to being available for guessing resulting type,
    #   even if the constraints are (initially) warns, not hard errors
    # see https://docs.sympy.org/latest/modules/functions/elementary.html
    if (
        expr.atoms(
            *SYMPY_ATOMS_FP
        ) or (
            # discover simple division
            # direct Integers are Rational, but fractional atoms are not Integer
            # additionally, simple divisions will simplify to Integer
            #   >>> parse_expr("4").atoms(Rational), parse_expr("4").atoms(Integer)
            #   ({4}, {4})
            #   >>> parse_expr("4/2").atoms(Rational), parse_expr("4/2").atoms(Integer)
            #   ({2}, {2})
            #   >>> e = "4/2*x + 1/3*y"
            #   >>> parse_expr(e).atoms(Rational) - parse_expr(e).atoms(Integer)
            #   {1/3}
            expr.atoms(sympy.Rational) - expr.atoms(sympy.Integer)
        ) or (
            # detect N/x constructs
            #   >>> srepr(parse_expr("2/x"))
            #   "Mul(Integer(2), Pow(Symbol('x'), Integer(-1)))"
            expr.match(sympy.Pow(sympy.Wild("", properties=[lambda a: a.is_Symbol or a.is_Function]), sympy.Integer(-1)))
        )
    ):
        if max_bitwidth <= 16:  # TODO is this a good assumption?
            return numpy.dtype("float32")
        return numpy.dtype("float64")

    # now pick the largest useful int
    # NOTE constant coefficients should all be Integer (Rational) if reached here

    w_signed   = 0  # NOTE Falsey
    w_unsigned = 0
    for dtype in dtypes_expr:
        if numpy.issubdtype(dtype, numpy.signedinteger):
            w_signed = max(w_signed, DTYPES_SUPPORTED[dtype])
        elif numpy.issubdtype(dtype, numpy.unsignedinteger):
            w_unsigned = max(w_unsigned, DTYPES_SUPPORTED[dtype])
        else:
            raise RuntimeError(f"BUG: failed to determine if {dtype} is a signed or unsigned int (is it a float?)")
    if w_signed and w_unsigned:
        raise TypeError("won't guess dtype for mixed int and uint, must be provided")
    if w_signed and not w_unsigned:
        return numpy.dtype("int64") if w_signed > 32 else numpy.dtype("int32")  # FUTURE >=
    if not w_signed and w_unsigned:
        return numpy.dtype("uint64") if w_unsigned > 32 else numpy.dtype("uint32")  # FUTURE >=

    raise RuntimeError(f"BUG: couldn't determine a good result dtype for {dtypes_expr}")


def get_result_dtype(expr_sympy, results, data, dtype_result=None):
    """ ensure the result datatype matches what's given if any
        use a reasonable guess when not provided explicitly or via result data array
    """
    if results:
        name_result = next(iter(results.keys()))  # NOTE dict of 1 value
        try:
            dtype_data_result = data[name_result].dtype
        except KeyError:  # name not in in data (not passed: create array later)
            dtype_data_result = None
        else:  # data array contains result for dtype, if expressly provided too, ensure they match
            if dtype_result is None:
                dtype_result = dtype_data_result
            else:
                if dtype_data_result != dtype_result:
                    raise ValueError(f"passed mismatched result array ({dtype_data_result}) and result dtype ({dtype_result})")

    # if dtype_result is still None, guess or raise
    if dtype_result is None:
        dtype_result = dtype_result_guess(expr_sympy, data)

    if dtype_result not in DTYPES_SUPPORTED:
        raise RuntimeError(f"BUG: dtype_result ({dtype_result}) not in DTYPES_SUPPORTED")

    # definitely a supported NumPy type now
    return dtype_result


def signature_automatic(expr, data, indexers=None, name_result=None):
    """ generate signature via naive Numba build """

    # TODO consider erroring if self-referential "r[n] = a[n] + r[n-1]"
    #   user must provide partially-filled result array, so type is already known
    #   still, this could warn them the type isn't what Numba expected

    # FIXME also verify with a given result_type?
    # FUTURE do safe casts and warn at completion?

    # remove indexing from the expr to avoid issues with basic lambdify
    if indexers:
        if len(indexers) != 1:
            raise ValueError("BUG: only a single indexer allowed if provided")
        indexer, (start, end) = next(iter(indexers.items()))
        slice_start = end - start      # start where values are likely to be valid
        slice_end   = slice_start + 1  # slice should always be [n:n+1]
        # NOTE checked during row build if this overruns the data `[1,2,3][5:6]` -> `[]`

        # trade all the indexed symbols (IndexedBase) for a direct Symbol
        replacements        = {}
        replacement_symbols = {}  # keep multiple instances consistent
        for atom in expr.atoms(sympy.Indexed):
            name = atom.atoms(sympy.IndexedBase).pop().name  # `a[i+1]` -> `"a"`
            try:
                sub_sym = replacement_symbols[name]
            except KeyError:
                sub_sym = sympy.Symbol(name)
                replacement_symbols[name] = sub_sym
            replacements[atom] = sub_sym
        expr = expr.subs(replacements)
    else:
        slice_start = None
        slice_end   = 1

    # FIXME this doesn't always work, especially when a result array is passed
    #   this is generally still part of [ISSUE 79] (see assorted follow-ups)
    # clobber expr with an equivalent one
    expr = expr.rhs
    args = sorted(s.name for s in expr.free_symbols)  # lexical sort matches other parses
    # if name_result is not None and name_result in data:
    #     args.append(name_result)
    #     expr = expr - sympy.Symbol(name_result)

    # make a new data table as if it only had 1 row, maintaining the inner shape and types
    data_1row = {}
    for name in args:  # avoids unused keys in data
        ref = data[name]
        if ref.ndim == 0:
            value = ref
        else:
            value = ref[slice_start:slice_end]
            if len(value) != 1:
                raise ValueError(f"data[{name}] with shape {ref.shape} doesn't have enough data to match combined offset({slice_start})")
        data_1row[name] = value

    # build callable and call it on single row
    fn = sympy.lambdify(args, expr)
    fn_jit = numba.jit(nopython=True)(fn)
    fn_jit(**data_1row)  # dynamic compile generates signature as a property
    # NOTE result ignored and might be [NaN], but the type and inner shape should be right

    # now extract signature
    count_signatures = len(fn_jit.nopython_signatures)
    if count_signatures != 1:  # should be impossible
        raise RuntimeError(f"BUG: unexpected signature count {count_signatures}: {fn_jit.nopython_signatures}")
    signature    = fn_jit.nopython_signatures[0]
    dtype_result = signature.return_type
    # coerce to NumPy type NOTE discards alignment
    dtype_result = numpy.dtype(str(dtype_result.dtype))  # numba.from_dtype(numpy.dtype("dtype")) for inverse

    return fn_jit, signature, dtype_result


def signature_generate(symbols, results, data, dtype_result):
    """ generate a signature like
          `Array(int64, 1d, C)(Array(int64, 1d, C))`
        note that Arrays can be named and they begin with the name "array", which
          `repr()` -> `array(int64, 1d, C)`

        refer to Numba types docs and Numba Array(Buffer) classes for more details
          https://numba.readthedocs.io/en/stable/reference/types.html
    """
    # FUTURE support for names (mabye an upstream change to numba)
    #   likely further C-stlye like `void(int32 a[], int64 b)`
    # without names, the dtypes are positional, so ordering must be maintained
    # within logic that could reorder the arguments after fixing the signature!
    # however, when the user calls the Expressive instance,
    # data is passed as kwargs `fn(**data)` to the inner function
    mapper = []

    if len(results) != 1:
        raise RuntimeError("BUG: results symbols should have exactly 1 member: {results}")
    name_result   = next(iter(results.keys()))  # NOTE dict of len==1 if given
    result_passed = bool(name_result in data)  # directly check membership

    names_symbols = list(symbols.keys())
    if not result_passed:
        names_symbols.pop()  # drop the result name (guaranteed to be last symbol in dict)
    for name in names_symbols:  # use symbol ordering, not data ordering
        ref   = data[name]
        field = numba.typeof(ref)  # `numba.types.Array(dtype, dims, layout)` or scalar type
        mapper.append(field)

    # TODO consider warning the user that dummy symbols in the data won't be used
    # NOTE collection only contains symbols which are exclusively a dummy
    # dummy_symbols_in_data = {s.name for s in symbols_dummy if s.name in data}
    # if dummy_symbols_in_data:
    #     warn(f"dummy symbols in data will be ignored: {dummy_symbols_in_data}")
    # TODO warn or raise if not all data names used (+config) [ISSUE 43]
    #   len() is sufficient (KeyError earlier if fewer, but may wrap that too)

    # discover result array dimensions
    if result_passed:
        dims = set(data[name].ndim for name in names_symbols if (name != name_result and data[name].ndim != 0))
        ndim_result = data[name_result].ndim
        if dims:  # ignore special case where only single values were passed
            # if len(dims) != 1:
            #     warn(f"unequal data dimensions may result in an error: {dims}")
            if ndim_result not in dims:
                raise ValueError(f"result dimensions (ndim={ndim_result}) do not match inputs: {dims}")
    else:
        dims = set(data[name].ndim for name in names_symbols) - {0}
        if not dims:  # should be detected in `data_cleanup`
            raise RuntimeError("BUG: impossible code path reached, cannot determine result array length from input arrays")
        if len(dims) != 1:
            raise ValueError(f"couldn't determine result dimensions from data, please provide a result array: {dims}")
        ndim_result = dims.pop()

    # now build complete signature for Numba to compile
    # FUTURE consider support for additional dimensions in result
    dtype = getattr(numba.types, str(dtype_result))
    return numba.types.Array(dtype, ndim_result, "C")(*mapper), result_passed


def verify_indexed_data_vs_symbols(symbols, result_passed, data):
    """ if this instance is indexed, make sure the data makes sense for it
        for example, with "a + b[i]", `a` must be a single value and `b` must be an array

        TODO consider if this should be merged with `signature_generate()`
    """
    names_symbols = list(symbols.keys())
    if not result_passed:
        names_symbols.pop()  # drop the result name (guaranteed to be last symbol in dict)

    for name in names_symbols:
        symbol = symbols[name]
        dims   = data[name].ndim
        if isinstance(symbol, sympy.IndexedBase) and dims == 0:
            raise ValueError(f"'{name}' is indexed, but is a single (ndim={dims}) value in data")
        if isinstance(symbol, sympy.Symbol) and dims > 0:
            title = {1: "array", 2: "matrix"}.get(dims, "tensor")
            raise ValueError(f"'{name}' is not indexed, but passed {title} (ndim={dims}) value in data")


def get_filler_result(dtype_result):
    """ determine a sensible fill value when creating a result array
        only called when
         - using indexing (indexers exists)
         - result array wasn't passed (whatever content it has is used)
        see also DTYPES_SUPPORTED
    """
    return {
        # numpy.dtype("bool"):,  # FUTURE (probably fail hard and force filling)
        numpy.dtype("uint8"):  0,
        numpy.dtype("uint16"): 0,
        numpy.dtype("uint32"): 0,
        numpy.dtype("uint64"): 0,
        numpy.dtype("int8"):  -1,
        numpy.dtype("int16"): -1,
        numpy.dtype("int32"): -1,
        numpy.dtype("int64"): -1,
        numpy.dtype("float32"): numpy.nan,
        numpy.dtype("float64"): numpy.nan,
        numpy.dtype("complex64"):  numpy.nan,
        numpy.dtype("complex128"): numpy.nan,
    }[dtype_result]


def breakout_Sum_to_loop(expr, symbols, indexers, results, name_result, data, attempt_simplify):
    """ better take on reducing Sum instances
    """
    if indexers or expr.atoms(sympy.Indexed):
        raise RuntimeError("BUG: escaped indexers (should be impossible): {indexers} vs {expr.atoms(sympy.Indexed)}")

    # collection of `Sum()` instances to work with and replace
    exprs_sums = expr.atoms(sympy.Sum)

    if attempt_simplify:
        # FUTURE `.simplify()` (and `summation()`?) can take an indefinite amount of time, consider
        #  - simple timeout [ISSUE 99] (warn user might optimize, then continue with loop functions?)
        #    consider `fork()` or multiprocessing so `simplify()` can be killed after timeout
        #  - tuning `ratio` arg
        #  - additional custom heuristics for `measure`, perhaps just marking `Sum()`
        threaded_timeout_warn = CONFIG["translate_simplify"]["build"]["sum"]["threaded_timeout_warn"]
        if threaded_timeout_warn:
            # FUTURE warn for each `sum_block()` so with several the problematic one can be identified
            def watcher_simplify_warn(e, timeout):
                e.wait(timeout)
                if not e.is_set():
                    warn(f"failed to simplify Sum() in expr after {timeout}s (may be hung)")

            event_watcher  = threading.Event()
            thread_watcher = threading.Thread(target=watcher_simplify_warn, args=(event_watcher, threaded_timeout_warn), daemon=True)
            thread_watcher.start()

        for sum_block in exprs_sums:
            sum_evaluated = sum_block.replace(sympy.Sum, sympy.summation)
            if not sum_evaluated.atoms(sympy.Sum):  # successfully decomposed `Sum()`
                # attempt to simplify numeric intermediates if any floating-point Atoms are used
                # as the result will be a Float and ideally the precision will remain the same
                #   >>> e = parse_expr("Sum(log(x/b), (x,1,10))")
                #   >>> e.doit()  # more precise, but may require many operations
                #   log(1/b) + log(2/b) + log(3/b) + log(4/b) + log(5/b) + log(6/b) + log(7/b) + log(8/b) + log(9/b) + log(10/b)
                #   >>> e.doit().simplify()      # 10! already exceeds 2**16
                #   10*log(1/b) + log(3628800)
                #   >>> e.doit().simplify().n()  # simplified
                #   10.0*log(1/b) + 15.1044125730755
                # NOTE evaluated functions which simplify to a number become `Float`, so
                #   this won't affect the result dtype
                # FUTURE does this make sense to apply to all inputs?
                #   probably not, but some subset could benefit
                if sum_evaluated.atoms(*SYMPY_ATOMS_FP):
                    # FIXME function instead of method used to ease test mocks
                    sum_evaluated = sympy.simplify(sum_evaluated).n()
                expr = expr.replace(sum_block, sum_evaluated)
                continue  # next sum_block

        if threaded_timeout_warn:
            event_watcher.set()
            thread_watcher.join()

        if not expr.atoms(sympy.Sum):  # successfully simplified all Sum() instances
            block_sum_functions = ""
            return expr, symbols, indexers, results, block_sum_functions

    # iterate to extract dummy vars and raise for problematic structures
    dummy_symbols = {}
    for sum_block in exprs_sums:
        fn_sum = sum_block.function
        limits = sum_block.limits  # tuple of tuples
        # separate and compare limit features
        dummy_var, limit_start, limit_stop = limits[0]

        # keep a collection of all dummy_symbols
        # TODO can this use `dummy_symbols_split()` result? (mostly avoiding KeyError from data[dummy])
        dummy_symbols[dummy_var.name] = dummy_var

    # define a new indexer
    # from string import ascii_lowercase as abcdefghijklmnopqrstuvwxyz
    # next(n for n in "abcdefghijklmnopqrstuvwxyz" if n not in symbols)
    for char_try in " abcdefghijklmnopqrstuvwxyz":
        indexer = f"idx_{char_try}".rstrip("_ ")  # "idx_ " -> "idx"
        if indexer not in symbols and indexer not in dummy_symbols:  # string compare
            indexer = sympy.Idx(indexer)  # prepare for mirroring
            break  # success: keep it for later
    else:  # didn't find any valid indexer
        raise ValueError(f"couldn't find a suitable indexer, all ascii lowercase characters used in expr: {symbols}")

    # identify and prepare to convert all vector/tensor Symbols to IndexedBase
    indexers.update({indexer: [0, 0]})  # always have 0 spread
    offset_values = {}
    indexed_variants = {}
    sum_functions = {}
    for name, symbol in symbols.items():
        if name in dummy_symbols:  # dummy members will redefined later
            # continue  # FUTURE nested Sum() instances probably need/support this
            raise RuntimeError(f"BUG: problematic ref is a Symbol and dummy var: {name}")
        base = sympy.IndexedBase(name)
        try:
            if data[name].ndim == 0:
                continue
        except KeyError as ex:       # might be the result name when not passed in data
            if name not in results:  # this should be impossible
                raise RuntimeError(f"BUG: unknown Symbol '{name}' not in data({data.keys()}): {repr(ex)}")
        offset_values[name]      = base
        indexed_variants[symbol] = sympy.Indexed(base, indexer)

    # TODO is it possible for there to be no offset_values?
    #   I think this can only happen if all values are singular and a result array is given
    #   otherwise no result length can be determined
    #   though it is possible for an individual `Sum()` to avoid having any

    # FUTURE support and reorder Sum instances to best order if they're nested (consider recursion too)
    #   trivially, maybe `sort()` where key is the count of Sum() atoms and then lexically?
    #   will this already handle outer dummy vars? probably

    # for each Sum(), create a new custom Function which simply iterates across each dummy in its range
    # sum_functions = {}  # FIXME moved above to inject converters for ndim=0 [ISSUE 120]
    mapper_new_Sum_functions = {}
    for index, sum_block in enumerate(exprs_sums):
        fn_sum = sum_block.function
        limits = sum_block.limits  # tuple of tuples
        dummy_var, limit_start, limit_stop = limits[0]

        # discover and fill arguments
        args = {s.name: s for s in fn_sum.atoms(sympy.Symbol) - {dummy_var}}
        args = {name: args[name] for name in sorted(args.keys())}  # rebuild in lexical order
        if not args:  # FIXME should only be possible if algebraic convert is skipped
            warn(f"Sum() has no non-dummy symbols (skipped simplification?): {sum_block}")

        # TODO consider crushing sum_block to be a safe name then collection + numbering
        # TODO prefix with 0 for length of exprs_sums
        fn_name = f"SumLoop{index}"

        result_dtype_sum = dtype_result_guess(fn_sum, data)  # returns a type like numpy.foo

        # TODO needs some careful analysis about `stop` vs `stop+1` syntax
        # NOTE Symbols are not replaced by IndexedBase instances yet and frozen as-is here
        T = f"""
        def {fn_name}(start, stop, {", ".join(args.keys())}):
            row = numpy.{str(result_dtype_sum)}(0)
            for {dummy_var} in range(start, stop+1):
                row += {fn_sum}  # don't use `row = row+..` to avoid assignment
            return row
        """

        # NOTE start and end can independently be Symbol or numeric
        F = sympy.Function(fn_name)(limit_start, limit_stop, *args.values())
        sum_functions[F] = text_dedent(T)  # maps Function to per-row finalized string

        # create a new Function with indexed args which when embedded will refer to the new loop
        F_indexed = sympy.Function(F.name)(*map(
            lambda a: indexed_variants.get(a, a),
            (limit_start, limit_stop, *args.values())
        ))
        mapper_new_Sum_functions[sum_block] = F_indexed

    # make a single block of string functions to embed as closure(s)
    block_sum_functions = "\n".join(sum_functions.values())

    # rewrite each `Sum()` instance in expr with indexed versions with the new name
    for sum_block, F_new in mapper_new_Sum_functions.items():
        expr = expr.replace(sum_block, F_new)

    # update symbols and the result value
    symbols.update(offset_values)
    expr = expr.replace(results[name_result], sympy.Indexed(symbols[name_result], indexer))

    return expr, symbols, indexers, results, block_sum_functions


def loop_function_template_builder(expr, symbols, indexers, results, result_passed, dtype_result, data):
    """ generate environment and code to support the function
         - create namespace
         - fill template
         - exec() to generate the code
         - extract new function
    """

    # get ready to build the template (note dict of len==1)
    name_result = next(iter(results.keys()))

    if not expr.atoms(sympy.Sum):
        block_sum_functions = ""
    else:
        # experimental Sum removal
        expr, symbols, indexers, results, block_sum_functions = breakout_Sum_to_loop(
            expr,
            symbols,
            indexers,
            results,
            name_result,
            data,
            CONFIG["translate_simplify"]["build"]["sum"]["try_algebraic_convert"],
        )

    # build namespace with everything needed to support the new callable
    # simplified version of sympy.utilities.lambdify._import
    _, _, translations, import_cmds = lambdify_modules["numpy"]
    expr_namespace = {"I": 1j}  # alt `copy.deepcopy(lambdify_modules["numpy"][1])`
    for import_line in import_cmds:
        exec(import_line, expr_namespace)
    # NOTE older SymPy versions may not have any translations at all
    #   while the latest seems to be just `{'Heaviside': 'heaviside'}`
    #   however, this is left as a trivial case for my multi-version build+test tool,
    #   which detects this as a line that is not run and has no other testing
    for sympyname, translation in translations.items():
        expr_namespace[sympyname] = expr_namespace[translation]

    # construct further template components
    names_symbols = list(symbols.keys())
    if not result_passed:
        # drop the result from arguments
        names_symbols.pop()

    block_args = ", ".join(names_symbols)

    # FUTURE manage this with uneven arrays if implemented [ISSUE 10]
    # NOTE this will use the first discovery it can as arrays all have the same length
    #   or will not pass `data_cleanup()`
    if result_passed:  # go ahead and use the passed array if possible
        name_size_symbol = name_result
    else:
        atom = sympy.IndexedBase if indexers else sympy.Symbol
        for symbol in expr.rhs.atoms(atom):
            name_symbol = symbol.name
            if name_symbol == name_result:  # result not passed so it can't be used (earlier check)
                continue  # pragma nocover FIXME ordering depends on hash seeding PYTHONHASHSEED
            name_size_symbol = name_symbol
            break
        else:  # this should have been verified in `data_cleanup()` or `verify_indexed_data_vs_symbols()`
            raise ValueError("BUG: couldn't determine size of result array, at least one symbol must be an array or pass a result array to fill")

    # prepare values to fill template
    if indexers:
        block_result = ""      # if the result array is passed in, just fill it by-index
        if not result_passed:  # without it, dynamically create an array of discovered length
            result_filler = get_filler_result(dtype_result)
            block_result = f"{name_result} = numpy.full_like({name_size_symbol}, {result_filler}, dtype={dtype_result})"
        block_sum_functions = "\n" + text_indent(block_sum_functions, "    " * 3)  # TODO calculate indent
    else:  # not indexed
        # broadcast when a result array is provided
        # otherwise let LHS be created dynamically
        broadcast_opt = "[:]" if result_passed else ""

    # construct template
    # FUTURE consider errno or errno-like arg to retrieve extra information from namespace
    if not indexers:
        T = f"""
        def expressive_wrapper({block_args}):
            {expr.lhs}{broadcast_opt} = {expr.rhs}
            return {name_result}
        """
    elif len(indexers) == 1:
        indexer, (start, end) = next(iter(indexers.items()))
        start = -start  # flip start to be positive (no -0 in "normal" Python)
        # FIXME improve accounting for result LHS in range
        #   consider disallowing negative LHS offset, though it could be useful
        T = f"""
        def expressive_wrapper({block_args}):
            {block_sum_functions}
            length = len({name_size_symbol})
            {block_result}
            for {indexer} in range({start}, length - {end}):
                {expr.lhs} = {expr.rhs}
            return {name_result}
        """
    else:
        # FUTURE consider if it's possible to implement this as nested loops [ISSUE 91]
        raise RuntimeError(f"BUG: indexers must be len 1 when provided (see string_expr_to_sympy): {indexers}")

    # tidy up template
    T = text_dedent(T)

    # build and extract
    exec(T, expr_namespace)
    fn = expr_namespace["expressive_wrapper"]

    return fn


def verify_cmp(data, expr_sympy, fn_python, fn_compiled, indexers):
    """ check if the compiled and python (pre-jit) functions have the same results
        this helps catch undefined behavior in Numba space, such as log(0)
    """
    # FIXME many magic numbers should be part of config subsystem [ISSUE 29]
    lengths = {k: (len(ref) if ref.ndim == 1 else 1) for k, ref in data.items()}
    lengths_max = max(lengths.values())
    data_names_containing_nan = []
    for name, ref in data.items():
        if numpy.isnan(ref).any():
            data_names_containing_nan.append(name)
    if data_names_containing_nan:
        warn(f"some data in {','.join(data_names_containing_nan)} is NaN")

    time_start = time.process_time_ns()
    result_py = fn_python(**data)
    time_py = time.process_time_ns() - time_start

    time_start = time.process_time_ns()
    result_nb = fn_compiled(**data)
    time_nb = time.process_time_ns() - time_start

    # hint user that using a lot of data
    if (time_py > 10 * NS10E9) and (lengths_max > 2000):
        warn(f"excessive data may be slowing native verify (python:{time_py / NS10E9:.2f}s, compiled:{time_nb}ns) (data lengths {lengths})")

    # check if either ran more than 30 seconds
    if (time_py >= 30 * NS10E9) or (time_nb >= 30 * NS10E9):
        warn(f"verify took a long time python:{time_py / NS10E9:.2f}s, compiled:{time_nb / NS10E9:.2f}s")

    # hint that just NumPy might actually be faster
    if lengths_max >= 1000:
        if time_nb / time_py > 2:  # NumPy is at least twice as fast
            warn(f"compiled function ({time_nb}ns) may be slower than direct NumPy ({time_py}ns) (data lengths {lengths})")

    # symbolics -> Number -> evalf()
    # FUTURE consider collecting Exceptions into a single warning reporting multiple rows
    result_sp = None
    if not indexers and all(d.ndim <= 1 for d in data.values()):  # no indexed values or tensors
        # NOTE numpy.nan are never equal, while sympy.nan are structurally equal, but not symbolically
        #   >>> numpy.nan == numpy.nan
        #   False
        #   >>> sympy.nan == sympy.nan
        #   True
        #   >>> sympy.Eq(numpy.nan, numpy.nan)
        #   False
        #   >>> sympy.Eq(sympy.nan, sympy.nan)
        #   False
        # NOTE numpy.log() handling of negative/zero values is -inf, not a complex value
        # so `sympy.zoo` is converted to `-numpy.inf`, not something like `numpy.complex64(numpy.inf)`
        # however, it might be worth considering `numpy.emath.log()`, which returns the "principle value"
        #   >>> sympy.log(0)
        #   zoo
        #   >>> numpy.log(0)
        #   -inf
        #   >>> numpy.emath.log(0)
        #   -inf
        #   >>> sympy.log(-1)
        #   I*pi
        #   >>> numpy.log(-1)
        #   nan
        #   >>> numpy.emath.log(-1)
        #   3.141592653589793j
        mapper_incomparable_sympy_results = {
            sympy.oo:   numpy.inf,
            sympy.zoo: -numpy.inf,
            sympy.nan:  numpy.nan,
        }
        result_sp = []
        for ref in data.values():
            if ref.ndim == 1:
                length = len(ref)
                break
        else:  # should have been trapped in `data_cleanup(data)`
            dims = {name: ref.ndim for name, ref in data.items()}  # pragma nocover (helper for impossible path)
            raise RuntimeError(f"BUG: no values with ndim==1 passed somehow all single values or tensors: {dims}")
            # length = 1  # FUTURE if allowing single values
        for index in range(length):
            row = {}
            row_nan = False  # track if the row has nan
            for symbols in data.keys():  # needed to handle single values
                value = data[symbols] if data[symbols].ndim == 0 else data[symbols][index]
                if numpy.isnan(value):
                    row_nan = True
                    break
                row[symbols] = value

            if row_nan:  # row is broken, write nan and continue
                result_sp.append(numpy.nan)  # NOTE sympy.nan are equal
                continue  # next row
            # directly use result as `Eq(LHS,RHS)` when no indexers are passed
            r = expr_sympy.rhs.subs(row).evalf()
            # print(f"row build {expr_sympy.rhs} -> {expr_sympy.rhs.subs(row)} -> {r}")  # debug
            if sympy.I in r.atoms():  # "3 * 1j" -> "3*I" -> "3j"
                r = complex(r)
            else:
                r = mapper_incomparable_sympy_results.get(r) or float(r)  # nan is not Falsey, 0->0.0
            result_sp.append(r)

    if indexers:
        indexer, (start, end) = next(iter(indexers.items()))
        start = -start
        end   = -end or None  # `1` to `-1`, `0` to `None`
        result = numpy.allclose(result_py[start:end], result_nb[start:end], equal_nan=True)
    elif result_sp:  # not indexed and no tensors
        result = []  # collection of bool
        for index in range(length):
            value_np, value_py, value_sp = result_nb[index], result_py[index], result_sp[index]
            r1 = numpy.allclose(value_np, value_py, equal_nan=True)
            r2 = numpy.allclose(value_py, value_sp, equal_nan=True)
            r3 = numpy.allclose(value_sp, value_np, equal_nan=True)
            result.append(r1 and r2 and r3)  # (this is a bool)
        result = all(result)  # compact collection into single bool
    else:  # tensor route
        try:
            length = next(len(ref) for ref in data.values() if ref.ndim > 1)
        except StopIteration:  # pragma nocover (impossible path)
            dims = {name: ref.ndim for name, ref in data.items()}
            raise RuntimeError("BUG: used tensor path, but no data had ndim>1: {dims}")
        result = []  # collection of bool
        for index in range(length):
            result.append(numpy.allclose(result_nb[index], result_py[index], equal_nan=True))
        result = all(result)  # compact collection into single bool

    results = {
        "nb": result_nb,
        "py": result_py,
        "sp": result_sp,
    }
    # print("results:")  # debug
    # print(results)

    if not result:  # FUTURE opportunity to hard fail here (via from config?) [ISSUE 29]
        raise RuntimeError(f"not allclose({result}) when comparing between NumPy and compiled function")
    return result, results


class Expressive:

    def __init__(self, expr, name_result=None, symbols=None, *, config=None, allow_autobuild=False):
        # FUTURE make cleanup optional (arg or config)

        symbols = symbols_given_cleanup(expr, symbols)

        if isinstance(expr, str):
            expr = string_expr_cleanup(expr)
            self._expr_sympy, self._symbols, self._indexers, self._results = string_expr_to_sympy(expr, name_result, symbols)
        elif isinstance(expr, (sympy.core.expr.Expr, sympy.core.relational.Equality)):
            self._expr_sympy, self._symbols, self._indexers, self._results = parse_sympy_expr(expr, name_result, symbols)
        else:
            raise ValueError(f"unexpected expr type({type(expr)}), must be str or SymPy Expr")

        # TODO config subsystem [ISSUE 29]
        "config hoopla"
        self.allow_autobuild = allow_autobuild

        # take any dummy symbols out of collection as they're not required in data
        self._symbols, self._symbols_dummy = dummy_symbols_split(self._expr_sympy, self._symbols)

        self._verifications = {}  # FIXME unstable contents for now
        self.signatures_mapper = {}

    def __str__(self):
        # NOTE unstable result for now
        return f"{type(self).__name__}({self._expr_sympy})"

    def __repr__(self):
        # NOTE unstable result for now
        # FUTURE display some major config settings (but most in a dedicated output)
        # FUTURE consider how to support or use `sympy.srepr()`
        content = [
            f"build_signatures={len(self.signatures_mapper)}",
            f"allow_autobuild={self.allow_autobuild}",
        ]
        return f"{str(self)} <{','.join(content)}>"

    def _repr_html_(self):
        """ dedicated Jupyter/IPython notebook pretty printer method
            this is loaded into an iframe, so mathjax is dynamically acquired too
            in order to render the LaTeX output from SymPy
        """
        # NOTE unstable result for now

        expr_latex = self._expr_sympy._repr_latex_()

        # ensure expr can be displayed properly
        # output wrapped by $$ is the normal output, however, it causes the result to be centered
        # instead, \(expr\) form is preferred which makes the result "inline" and aligned as parent
        expr_latex = re.sub(r"^\$\$?([^\$]+)\$\$?$", r"\(\1\)", expr_latex)
        if not (expr_latex.startswith(r"\(") and expr_latex.endswith(r"\)") and len(expr_latex) >= 5):
            warn(rf"unexpected expr format (should be wrapped in $ -> \(\)): {expr_latex}")
            return repr(self)

        # TODO improved templating (though I want to keep deps low)
        #   consider some template engine when available
        # generated as-suggested on mozilla https://developer.mozilla.org/en-US/docs/Web/Security/Subresource_Integrity
        #   `cat src/tex-chtml.js | openssl dgst -sha384 -binary | openssl base64 -A`
        # https://github.com/mathjax/MathJax 3.2.2@227c4fecc0037cef1866d03c64c3af10b685916d
        # see also https://github.com/mathjax/MathJax-src
        template = """
        <!DOCTYPE html>
        <html>
        <head>
        <script type="text/javascript" id="MathJax-script"
            src="https://cdn.jsdelivr.net/npm/mathjax@3.2.2/es5/tex-chtml.js"
            integrity="sha348-AHAnt9ZhGeHIrydA1Kp1L7FN+2UosbF7RQg6C+9Is/a7kDpQ1684C2iH2VWil6r4"
            crossorigin="anonymous"></script>
        </head>
        <body>
        <ul style="list-style-type:none;padding-left:0;">
        {html_list}
        </ul>
        </body>
        </html>
        """

        # stack entries in unordered list
        collected_values = [
            expr_latex,  # advanced representation
            repr(self),  # FIXME unstable
        ]
        html_list = "\n    ".join(f"<li>{html_escape(a)}</li>" for a in collected_values)

        # fill template
        content = text_dedent(template.format(
            html_list=html_list,
        ))

        return content

    def _prepare(self, data, dtype_result):
        """ prepare before build or __call__ """
        data = data_cleanup(data)
        dtype_result = get_result_dtype(self._expr_sympy, self._results, data, dtype_result)
        signature, result_passed = signature_generate(self._symbols, self._results, data, dtype_result)
        if self._indexers:  # when indexed, the data shape (array vs single values) matter much more
            verify_indexed_data_vs_symbols(self._symbols, result_passed, data)
        return data, dtype_result, signature, result_passed

    def build(self, data, *, dtype_result=None, verify=None):  # arch target?
        """ compile function and collect it in signatures_mapper """
        data, dtype_result, signature, result_passed = self._prepare(data, dtype_result)

        # automatically set to verify when the array is small
        # only happens for pre-builds as __call__ sets `verify=False` when autobuilding
        if verify is None:
            # approximate max array length (ignores offsets)
            lengths_max = max((len(ref) if ref.ndim == 1 else 1) for ref in data.values())
            if lengths_max <= 50:  # FIXME magic numbers to config subsystem [ISSUE 29]
                verify = True

        # generate Python function
        expr_fn = loop_function_template_builder(
            self._expr_sympy,
            self._symbols,
            self._indexers,
            self._results,
            result_passed,
            dtype_result,
            data,
        )

        # pre-compile function as the signature is given
        # FUTURE collect into a class with additional properties (just build time?)
        built_function = numba.jit(
            signature,
            nopython=True,  # now the default
            # fastmath=True,  # FUTURE config setting [ISSUE 29]
            parallel=True,  # FUTURE config setting [ISSUE 29]
        )(expr_fn)

        if verify:
            result, results = verify_cmp(data, self._expr_sympy, expr_fn, built_function, self._indexers)
            # self._verifications[signature] = result, results  # unstable contents for now

        self.signatures_mapper[signature] = built_function

        # FUTURE does it make sense to return the result(s) from verify?
        #   return self, {"py": result_py, "nb": result_nb, "sp": result_sp}
        # no: probably better to make the result(s) a new property
        return self  # enable dot chaining

    def __call__(self, data, dtype_result=None):
        """ call the relevant compiled function for a particular data collection on it
            if signatures_mapper doesn't have the signature, allow_autobuild can be used
            to create it dynamically, though this loses a lot of the runtime execution speed
            benefits available to users who are able to pre-build for all the data
            signatures they have
        """
        data, dtype_result, signature, result_passed = self._prepare(data, dtype_result)

        try:
            fn = self.signatures_mapper[signature]
        except KeyError:
            if not self.allow_autobuild:
                raise KeyError("no matching signature for data: use .build() with representative sample data (or set allow_autobuild=True)")
            # FUTURE improve warning subsystem (never, once, each, some callback, etc.)
            #   further opportunity for dedicated config features
            # really it's important to alert users to a potential error, but not nanny 'em
            time_start = time.process_time()
            self.build(data, dtype_result=dtype_result, verify=False)
            time_build = time.process_time() - time_start
            warn(f"autobuild took {time_build:.2f}s of process time, prefer .build(sample_data) in advance if possible")
            try:
                fn = self.signatures_mapper[signature]
            except KeyError:  # pragma nocover - bug path
                raise RuntimeError("BUG: failed to match signature after autobuild")

        return fn(**data)
