# Benchmark Functions: a Python Collection
A benchmark functions collection written in Python 3.X, suited for assessing the performances of optimisation problems on deterministic functions. Most functions here implemented can be created in an arbitrary number of dimensions (i.e. $`R^N\to R`$). Suggested boundaries, as well the values of known minima/maxima, are also provided. Finally, every function can be visualised with an interactive widget.

Please check out the [companion paper](https://arxiv.org/abs/2406.16195) for more information.

## Installation
This module is available on [pip](https://pypi.org/project/benchmark-functions) and can be installed as follows:
```sh
$ pip3 install benchmark_functions
```

## Usage
To use a function from the collection it is sufficient to instantiate the relative class from the library:
```python
import benchmark_functions as bf

func = bf.Schwefel(n_dimensions=4)
```
Most functions impelmented can be instantiated with an arbitrary number of dimensions. This can be set with a  *n_dimensions* optional parameter. If the numer of dimensions are not specified a default value (generally $`N=2`$) will be used.
Some functions require other specific parameters (e.g. Ackley), these can be set in the constructor, otherwise default values will be taken.
Some functions are only defined for 2 dimensions (e.g. Easom) in these cases no *n_dimensions* parameter is accepted.

Calling directly the instantiated function on a point will provide the function's value:
```python
point = [25, -34.6, -112.231, 242]
func(point) # results in -129.38197657025287
```
The call will perform some internal sanity checks on the passed point, like its dimensionality and type. If you are reasonably sure about the values of your points and want to improve the computational performances, you can pass the *validate=False* flag when calling the function.

Normally, these functions are used as a minimisation problem, so they are designed accordingly.
An optional flag **opposite** can be passed in any function constructor.
If set to *True* the value of the function will be the opposite at each call. The values of the **minima/um** and **maxima/um** functions (see below) are modified accordingly.
This is meant to streamline the  use of a maximisation algorithm on these functions.
### Convenience Functions
A set of convenience functions are also implemented in the class, namely:

- **name** the name of the function;
- **minima**/**maxima** returns a list of *Optimum* objects of the known global minima/maxima. If any value is unknown, a *None* value will be present instead;
- **minimum**/**maximum** returns a single *Optimum* of the known global minimum/maximum. If any value is unknown, a *None* value will be present instead;
- **suggested_bounds** returns a tuple of two elements (*LB*, *UB*) each one is a list of *n_dimensions* elements, representing the suggested search boundary of the function;
- **show** plot the function in an interactive graphic widget. Read the relative section below for more information on this feature;

As an example, the following code:
```python
print(func.suggested_bounds())
```
will produce
```
([-500.0, -500.0, -500.0, -500.0], [500.0, 500.0, 500.0, 500.0])
```
for the Schwefel function.
### Known minima/maxima
The minima returned are the ones known and generally considered relevant for the function. In most cases, you should expect to always find included in the list at least the global minimum (if it is known) along some extra local minima that can be useful in assessing optimisation results. Examples are the minima present in the De Jong 5 and Michalewicz functions. In the same fashion, interesting known local maxima are also available.

*Optimum* is a class that contains the following attributes:
- **position** a list with the coordinates;
- **score** the value of the optimum in the function;
- **type** that is one of: 'Minimum', 'Maximum' or 'Saddle';
- **region_type** the type of region the optimum is located. It can be one of: 'Convex', 'Concave', 'Plateau', 'Saddle' or 'Unknown';

Generally a function global minimum/maximum can change with the number of dimensions. For this reason some **minima**/**maxima** values may be missing or inaccurate. If you find a better global optimum please open an issue about that with the coordinates and I'll update the library (see the relevant sections below).

### Baseline Search Techniques
Two simple search techniques are also provided out-of-the-box and are available for every function:
- **minimum_random_search** performs a random search and returns the local minimum point as tuple *(point, score)* within the boundaries provided by the parameter *bounds*. If several minima points with the same score are found (e.g. the local minimum is in a plateau) a list of points will be provided instead. The *n_samples* parameter (set to $`10^7`$ by default) specifies the number of samplings performed.
- **minimum_grid_search** performs a random search and returns the local minimum point as tuple *(point, score)* within the boundaries provided by the parameter *bounds*. If several minima points with the same score are found (e.g. the local minimum is in a plateau) a list of points will be provided instead. The optional parameter *n_edge_points* (set to 100 by default) defines the number of points of the grid "edge", meaning that the actual number of points assessed are $`(n_edge_points+1)^N`$. This function is lightweight in terms of memory, since the grid is created and iterated in place, however it can require a lot of computational time due to the big number of function's evaluations.

These techniques are not efficient nor effective, and they are provided only as potential baseline for comparing intelligent optimisation techniques. 
For an example of optimisation with the [Bees Algorithm](https://gitlab.com/bees-algorithm/bees_algorithm_python) please refer to [this](https://gitlab.com/luca.baronti/python_benchmark_functions/-/snippets/2046262) and [this](https://gitlab.com/luca.baronti/python_benchmark_functions/-/snippets/2046282) snippets.

### Visualise a function
Using the *show* function will plot the benchmark function in an interactive widget.
This can be done only if the *n_dimensions* is lower than 3. The resulting plot is either a 3D surface (when *n_dimensions=2*) or a simple 2D graph plot (*n_dimensions=1*). If the function is defined in 2 dimensions, it is also possible to plot it as an heatmap setting the function parameter *asHeatMap=True* as follows:
```python
func.show(asHeatMap=True)
```
By default, the function will be shown according to the suggested boundaries. It is possible to pass custom boundaries for visualisation purpose using the parameter *bounds*.
The curve/surface is interpolated according to a number of points uniformly sampled within the considered boundaries. The number of $`N\times N`$ points can be tuned passing the $`N`$ value to the parameter *resolution* (by default $`N=50`$). 

A list of points can be optionally plotted along the main function plot, assigning it to the parameter *showPoints*. For instance, the following call will display the function along all the known local minimima:
```python
func.show(showPoints=func.minima())
```

Note: whilst importing and using the library require nothing more than the *numpy* python library, in order to visualise the functions the *matplotlib* library is also required.

## List of Available Functions and Expandability Features

For a list of available functions, instructions to expand the library and other information please refer to the [project homepage](https://gitlab.com/luca.baronti/python_benchmark_functions).


## Author and License

This library is developed and maintained by Luca Baronti (**gmail** address: *lbaronti*) and released under [GPL v3 license](LICENSE).

If you are using this tool for your work, please cite the [companion paper](https://arxiv.org/abs/2406.16195) using this reference:
```
@misc{baronti2024python,
      title={A Python Benchmark Functions Framework for Numerical Optimisation Problems}, 
      author={Luca Baronti and Marco Castellani},
      year={2024},
      eprint={2406.16195},
      archivePrefix={arXiv},
      primaryClass={id='math.NA' full_name='Numerical Analysis' is_active=True alt_name='cs.NA' in_archive='math' is_general=False description='Numerical algorithms for problems in analysis and algebra, scientific computation'}
}
```