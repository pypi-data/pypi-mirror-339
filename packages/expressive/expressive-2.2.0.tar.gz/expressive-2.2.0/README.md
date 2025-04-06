# expressive

A library for quickly applying symbolic expressions to NumPy arrays

By enabling callers to front-load sample data, developers can move the runtime cost of Numba's JIT to the application's initial loading (or an earlier build) and also avoid `exec` during runtime, which is otherwise needed when lambdifying symbolic expressions

Inspired in part by this Stack Overflow Question [Using numba.autojit on a lambdify'd sympy expression](https://stackoverflow.com/questions/22793601/using-numba-autojit-on-a-lambdifyd-sympy-expression)

## installation

via pip https://pypi.org/project/expressive/

```shell
pip install expressive
```

## usage

refer to tests for examples for now

generally follow a workflow like
* create instance `expr = Expressive("a + log(b)")`
* build instance `expr.build(sample_data)`
* instance is now callable `expr(full_data)`

the `data` should be provided as dict of NumPy arrays

 ```python
data_sample = {  # simplified data to build and test expr
    "a": numpy.array([1,2,3,4], dtype="int64"),
    "b": numpy.array([4,3,2,1], dtype="int64"),
}
data = {  # real data user wants to process
    "a": numpy.array(range(1_000_000), dtype="int64"),
    "b": numpy.array(range(1_000_000), dtype="int64"),
}
E = Expressive("expr")  # string or SymPy expr
E.build(data_sample)  # data's types used to compile a fast version
E(data)  # very fast callable
```

simple demo

```python
import time
import contextlib
import numpy
import matplotlib.pyplot as plt
from expressive import Expressive

# simple projectile motion in a plane
E_position = Expressive("y = v0*t*sin(a0) + 1/2(g*t^2)")

# expr is built early in the process runtime by user
def build():
    # create some sample data and build with it
    # the types are used to compile a fast version for full data
    data_example = {
        "v0": 100,  # initial velocity m/s
        "g": -9.81, # earth gravity m/s/s
        "a0": .785,  # starting angle ~45° in radians
        "t": numpy.linspace(0, 15, dtype="float64"),  # 15 seconds is probably enough
    }
    assert len(data_example["t"]) == 50  # linspace default
    time_start = time.perf_counter()
    E_position.build(data_example)  # verify is implied with little data
    time_run = time.perf_counter() - time_start

    # provide some extra display details
    count = len(data_example["t"])
    print(f"built in {time_run*1000:.2f}ms on {count:,} points")
    print(f"  {E_position}")

def load_data(
    point_count=10**8,  # 100 million points (*count of angles), maybe 4GiB here
    initial_velocity=100,  # m/s
):
    # manufacture lots of data, which would be loaded in a real example
    time_array = numpy.linspace(0, 15, point_count, dtype="float64")
    # collect the results
    data_collections = []
    # process much more data than the build sample
    for angle in (.524, .785, 1.047):  # initial angles (30°, 45°, 60°)
        data = {  # data is just generated in this case
            "v0": initial_velocity,  # NOTE type must match example data
            "g": -9.81, # earth gravity m/s/s
            "a0": angle,  # radians
            "t": time_array,  # just keep re-using the times for this example
        }
        data_collections.append(data)

    # data collections are now loaded (created)
    return data_collections

# later during the process runtime
# user calls the object directly with new data
def runtime(data_collections):
    """ whatever the program is normally up to """

    # create equivalent function for numpy compare
    def numpy_cmp(v0, g, a0, t):
        return v0*t*numpy.sin(a0) + 1/2*(g*t**2)

    # TODO also compare numexpr demo

    # call already-built object directly on each data
    results = []
    for data in data_collections:
        # expressive run
        t_start_e = time.perf_counter()  # just to show time, prefer timeit for perf
        results.append(E_position(data))
        t_run_e = time.perf_counter() - t_start_e

        # simple numpy run
        t_start_n = time.perf_counter()
        result_numpy = numpy_cmp(**data)
        t_run_n = time.perf_counter() - t_start_n

        # provide some extra display details
        angle = data["a0"]
        count = len(data["t"])
        t_run_e = t_run_e * 1000  # convert to ms
        t_run_n = t_run_n * 1000
        print(f"initial angle {angle}rad ran in {t_run_e:.2f}ms on {count:,} points (numpy:{t_run_n:.2f}ms)")

    # decimate to avoid very long matplotlib processing
    def sketchy_downsample(ref, count=500):
        offset = len(ref) // count
        return ref[::offset]

    # display results to show it worked
    for result, data in zip(results, data_collections):
        x = sketchy_downsample(data["t"])
        y = sketchy_downsample(result)
        plt.scatter(x, y)
    plt.xlabel("time (s)")
    plt.ylabel("position (m)")
    plt.show()

def main():
    build()
    data_collections = load_data()
    runtime(data_collections)

main()
```

![](https://gitlab.com/expressive-py/docs/-/raw/d1e43411242fda9cc81ced55484f9e7575acb6c3/img/expressive_examples_2d_motion.png)

## compatibility matrix

generally this strives to only rely on high-level support from SymPy and Numba, though Numba has stricter requirements for NumPy and llvmlite

| Python | Numba | NumPy | SymPy | commit | coverage | runtime |
| --- | --- | --- | --- | --- | --- | --- |
| 3.7.17 | 0.56.4 | 1.21.6 | 1.6 | 644c244 | {'expressive.py': '🟠 99% m 1144', 'test.py': '🟢 100%'} | 77s |
| 3.8.20 | 0.58.1 | 1.24.4 | 1.7 | 644c244 | {'expressive.py': '🟠 99% m 1144', 'test.py': '🟢 100%'} | 75s |
| 3.9.19 | 0.53.1 | 1.23.5 | 1.7 | 644c244 | {'expressive.py': '🟠 99% m 1144', 'test.py': '🟢 100%'} | 71s |
| 3.9.19 | 0.60.0 | 2.0.1 | 1.13.2 | 644c244 | 🟢 100% | 75s |
| 3.10.16 | 0.61.0 | 2.1.3 | 1.13.3 | 644c244 | 🟢 100% | 73s |
| 3.11.11 | 0.61.0 | 2.1.3 | 1.13.3 | 644c244 | 🟢 100% | 78s |
| 3.12.7 | 0.59.1 | 1.26.4 | 1.13.1 | 644c244 | 🟢 100% | 61s |
| 3.12.8 | 0.61.0 | 2.1.3 | 1.13.3 | 644c244 | 🟢 100% | 71s |
| 3.13.1 | 0.61.0 | 2.1.3 | 1.13.3 | 644c244 | 🟢 100% | 72s |

NOTE differences in test run times are not related to or an indicator of built expr speed (likely the opposite), and are more interesting as development changes

#### further compatibility notes

these runs build the package themselves internally, while my publishing environment is currently Python 3.11.2

though my testing indicates that this works under a wide variety of quite old versions of Python/Numba/SymPy, upgrading to the highest dependency versions you can will generally be best
* Python 3 major version status https://devguide.python.org/versions/
* https://numba.readthedocs.io/en/stable/release-notes-overview.html

NumPy 1.x and 2.0 saw some major API changes, so older environments may need to adjust or discover working combinations themselves
* some versions of Numba rely on `numpy.MachAr`, which has been [deprecated since at least NumPy 1.22](https://numpy.org/doc/stable/release/1.22.0-notes.html#the-np-machar-class-has-been-deprecated) and may result in warnings

TBD publish multi-version test tool

## testing

Only `docker` is required in the host and used to generate and host testing

```shell
sudo apt install docker.io  # debian/ubuntu
sudo usermod -aG docker $USER
sudo su -l $USER  # login shell to self (reboot for all shells)
```

Run the test script from the root of the repository and it will build the docker test environment and run itself inside it automatically

```shell
./test/runtests.sh
```

## build + install locally

Follows the generic build and publish process
* https://packaging.python.org/en/latest/tutorials/packaging-projects/#generating-distribution-archives
* build (builder) https://pypi.org/project/build/

```shell
python3 -m build
python3 -m pip install ./dist/*.whl
```

## contributing

The development process is currently private (though most fruits are available here!), largely due to this being my first public project with the potential for other users than myself, and so the potential for more public gaffes is far greater

Please refer to [CONTRIBUTING.md](https://gitlab.com/expressive-py/expressive/-/blob/main/CONTRIBUTING.md) and [LICENSE.txt](https://gitlab.com/expressive-py/expressive/-/blob/main/LICENSE.txt) and feel free to provide feedback, bug reports, etc. via [Issues](https://gitlab.com/expressive-py/expressive/-/issues), subject to the former

#### additional future intentions for contributing
* improve internal development history as time, popularity, and practicality allows
* move to parallel/multi-version/grid CI over all-in-1, single-version dev+test container (partially done with 2.0.0!)
* ~~greatly relax dependency version requirements to improve compatibility~~
* publish majority of ticket ("Issue") history

## version history

##### v2.2.0
* added support for the `Sum` function (SymPy unevaluated summation)
  * attempts to evaluate/decompose `Sum` into an algebraic expression during building `.build()`
  * creates a custom function to manage `Sum` instances which can't be simplified
  * spawn a thread to warn user when attempting to simplify a `Sum`s is taking an excessive amount of time (duration and even halting are unknown, so the user may not know where the issue is .. 20s default)
* added basic configuration system `CONFIG`
  * API is unstable and largely featureless, but needed to control/disable `Sum` simplifying
  * currently a singleton `dict` shared by all `Expressive` instances, but a future version/design will accept per-instance configurations and combine them with global defaults
* generally much better handling for scalars in data
  * scalar values are no longer coerced into a 0-dim array
  * NumPy scalars (not just Python numbers) are now allowed

##### v2.1.0 (unreleased)
* added a new `signature_automatic()` which (ab)uses the Numba JIT to determine the result's `dtype` even for indexed exprs

##### v2.0.0
* enabled matrix/tensor support
* improved/reduced warnings from verify
* tested + greatly reduced dependency version requirements
* added a basic usage example (uses new docs repo https://gitlab.com/expressive-py/docs/ )

##### v1.9.0
* improved package layout
* build and install package during `runtests.sh` (earlier versions use relative importing)
* improve errors around invalid data/Symbol names

##### v1.8.1
* fixed a regex bug where multidigit offset indicies could become multiplied `x[i+10]` to `x[i+1*0]`
* improve complex result type guessing

##### v1.8.0
* support for passing a SymPy expr (`Expr`, `Equality`), not just strings

##### v1.7.0
* support for passing SymPy symbols to be used

##### v1.6.1 (unreleased)
* support indexed result array filling for complex dtypes

##### v1.6.0
* complex dtypes MVP (`complex64`, `complex128`)
* parse coefficients directly adjacent to parentheses `3(x+1)` -> `3*(x+1)`

##### v1.5.1 (unreleased)
* improved README wording of [testing](#testing) and added [building section](#building)
* better messages when testing and `docker` is absent or freshly installed

##### v1.5.0
* added `._repr_html_()` method for improved display in Jupyter/IPython notebooks

##### v1.4.2
* greatly improved verify
  * `numpy.allclose()` takes exactly 2 arrays to compare (further args are passed to `rtol`, `atol`)
  * SymPy namespace special values `oo`, `zoo`, `nan` are coerced to NumPy equivalents (`inf`, `-inf`, `nan`)
  * raise when result is `False`
  * groundwork to maintain an internal collection of results
* internal symbols collection maintains `IndexedBase` instances (`e.atoms(Symbol)` returns `Symbol` instances)
* improve Exceptions from data that can't be used
* new custom warning helper for testing as `assertWarnsRegex` annoyingly eats every warning it can

##### v1.4.1
* more sensibly fill the result array for non-floats when not provided (only float supports NaN)

##### v1.4.0
* add build-time verify step to help identify math and typing issues
* some improved logic flow and improved `warn()`

##### v1.3.2 (unreleased)
* improved publishing workflow
* improved README

##### v1.3.1
* fix bad math related to indexing range
* add an integration test

##### v1.3.0
* add support for parsing equality to result
* add support for (optionally) passing result array
* hugely improve docstrings

##### v1.2.1
* add more detail to [contributing block](#contributing)
* switch array dimensions checking from `.shape` to `.ndim`
* switch tests from `numpy.array(range())` to `numpy.arange()`

##### v1.2.0
* enable autobuilding (skip explicit `.build()` call)
* basic display support for `Expressive` instances

##### v1.1.1
* add version history block

##### v1.1.0
* fixed bug: signature ordering could be unaligned with symbols, resulting in bad types
* added support for non-vector data arguments

##### v1.0.0
* completely new code tree under Apache 2 license
* basic support for indexed offsets

##### v0.2.0 (unreleased)

##### v0.1.0
* very early version with support for python 3.5
