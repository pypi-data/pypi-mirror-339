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

## List of Available Functions


Name | Image | Description
:---: | :---: | :---
Hypersphere | ![](pics/hypersphere.jpg) | A hypersphere centered in the origin. <br><div align="center">$`f(x)=\sum_{i=0}^{N-1} x_i^2`$</div>
Hyperellipsoid<sup>[5]</sup> | ![](pics/hyperellipsoid.jpg) | A rotated hyperellipsoid centered in the origin. <br><div align="center">$`f(x)=\sum_{i=0}^{N-1}\sum_{j=0}^{i} x_j^2`$</div>
Schwefel<sup>[2]</sup> | ![](pics/schwefel.jpg) |  Non-convex and (highly) multimodal. Location of the minima are geometrical distant.<br><div align="center">$`f(x)=418.9829 N\sum_{i=0}^{N-1} x_i\sin(\sqrt{\|x_i\|})`$</div>
Ackley<sup>[9]</sup> | ![](pics/ackley.jpg) |  Non-convex and multimodal. Clear global minimum at the center surrounded by many symmetrical local minima. Use three parameters a, b and c. <br><div align="center">$`f(x)=-a\exp\left(-b\sqrt{\frac{1}{N}\sum_{i=0}^{N-1} x_i^2}\right)-\exp\left(\frac{1}{N}\sum_{i=1}^N \cos(x_i c)\right)+a+e`$</div>
Michalewicz<sup>[1]</sup> | ![](pics/michalewicz.jpg) |  Non-convex and (highly) multimodal. Contains n! local minimum. Use a parameter $`m`$ that defines the stepness of the curves. Global minimum around f([2.2,1.57])=-1.8013 for n=2, f(x)=-4.687 for n=5 and f(x)=-9.66 for n=10 (no optimal solution given).<br><div align="center">$`f(x)=-\sum_{i=0}^{N-1} \sin(x_i)\sin^{2m}\left(\frac{x_i^2(i+1)}{\pi}\right)`$</div>
Rastrigin<sup>[3]</sup> | ![](pics/rastring.jpg) |  Non-convex and (highly) multimodal. Location of the minima are regularly distributed.  <br><div align="center">$`f(x)=10N+\sum_{i=0}^{N-1} (x_i^2 - 10\cos(2\pi x_i))`$</div>
Rosenbrock<sup>[3]</sup> | ![](pics/rosenbrock.jpg) |   Non-convex and unimodal. Global minimum difficult to approximate.<br><div align="center">$`f(x)=\sum_{i=0}^{N-2} (100(x_{i+1}-x_i^2)^2+(x_i-1)^2`$</div>
De Jong 3<sup>[12]</sup> |  ![](pics/dejong3.jpg) |   Multimodal, "stair"-like function, with multiple plateau at different levels. <br><div align="center">$`f(x)=\sum_{i=0}^{N-1} \lfloor x_{i}\rfloor `$</div>
De Jong 5<sup>[5]</sup> |  ![](pics/dejong5.jpg) |   Continuous, multimodal, multiple symmetric local optima with narrow basins on a plateau. It's defined only for 2 dimensions. <br><div align="center">$`f(x)=(0.002+\sum_{i=1}^{25} (i+(x_1-A_{1i})^6+(x_2-A_{2i})^6)^{-1}`$</div>
Martin and Gaddy<sup>[5]</sup> |  ![](pics/martin_gaddy.jpg) |   Unimodal, with a large single valley between two symmetrical peaks. It's defined only for 2 dimensions. <br><div align="center">$`f(x)=(x_1-x_2)^2+\left(\frac{x_1+x_2-10}{3}\right)^2`$</div>
Griewank<sup>[5]</sup> | ![](pics/griewangk600.jpg) |   Non-convex and (highly) multimodal, it shows a different behaviour depending on the scale (zoom) that is used. [zoom=0] general overview $`[-600 \leq x_i \leq 600]`$ suggests convex function <br><div align="center">$`f(x)=\sum_{i=0}^{N-1} \frac{x_i^2}{4000}- \prod_{i=0}^{N-1} \cos\frac{x_i}{\sqrt{i+1}}+1 `$</div>
---- | ![](pics/griewangk10.jpg) |   [zoom=1] medium-scale view $`[-10 \leq x_i \leq 10]`$ suggests existence of local optima
---- | ![](pics/griewangk5.jpg) |      [zoom=2] zoom on the details $`[-5 \leq x_i \leq 5]`$ indicates complex structure of numerous local optima
Easom<sup>[10]</sup> | ![](pics/easom.jpg) |      Unimodal, mostly a plateau with global minimum in a small central area. It's defined only for 2 dimensions. <br><div align="center">$`f(x)=-\cos(x_1)\cos(x_2)exp(-(x_1-\pi)^2-(x_2-\pi)^2) `$</div>
Goldstein and Price<sup>[6]</sup> | ![](pics/goldstein_price.jpg) | Multimodal with an asymmetrical hight slope and global minimum on a plateau. It's defined only for 2 dimensions.   <br><div align="center">$`f(x)=(1+(x_0+x_1+1)^2(19-14x_0+3x_0^2-14x_1+6x_0x_1+3x_1^2))\cdot(30+(2x_0-3x_1)^2(18-32x_0+12x_0^2+48x_1-36x_0x_1+27x_1^2)) `$</div>
Picheny, Goldstein and Price<sup>[6]</sup> | ![](pics/picheny_goldstein_price.jpg) | (logaritmic variant of Goldstein and Price) Non-convex, multimodal with multiple asymmetrical slopes and global minimum near local optima. It's defined only for 2 dimensions.  <br><div align="center">$`f(x)=2.427^{-1}(\log[(1+(x_0+x_1+1)^2(19-14x_0+3x_0^2-14x_1+6x_0x_1+3x_1^2))\cdot(30+(2x_0-3x_1)^2(18-32x_0+12x_0^2+48x_1-36x_0x_1+27x_1^2))]-8.693) `$</div>
Styblinski and Tang | ![](pics/styblinski_tang.jpg) | Multimodal, with optima displaced in a symmetric way. <br><div align="center">$`f(x)=0.5\sum_{i=0}^{N-1}(x_i^4-16x_i^2+x_i)`$</div>
Mc Cormick<sup>[7]</sup> | ![](pics/mccormick.jpg) | Unimodal, uneven slopes on the sides. It's defined only for 2 dimensions. <br><div align="center">$`f(x)=\sin(x_0+x_1)+(x_0-x_1)^2-1.5x_0+2.5x_1+1`$</div>
Rana<sup>[1]</sup> | ![](pics/rana.jpg) | Highly multimodal symmetric function. <br><div align="center">$`f(x)=\sum_{i=0}^{N-2}x_i\cos\sqrt{\|x_{i+1}+x_i+1\|}\sin\sqrt{\|x_{i+1}-x_i+1\|}+(1+x_{i+1})\sin\sqrt{\|x_{i+1}+x_i+1\|}\cos\sqrt{\|x_{i+1}-x_i+1\|}`$</div>
Egg Holder<sup>[1]</sup> | ![](pics/eggholder.jpg) | Non-convex, contains multiple asymmetrical local optima. <br><div align="center">$`f(x)=-\sum_{i=0}^{N-2}(x_{i+1}+47)\sin\sqrt{\|x_{i+1}+47+0.5x_i\|}+x_i\sin\sqrt{\|x_i-(x_{i+1}+47)\|}`$</div>
Keane<sup>[1]</sup> | ![](pics/keane.jpg) | Mutlimodal funciton with local optima regions of different depth.<br><div align="center">$`f(x)=-(\|\sum_{i=0}^{N-1}\cos^4x_i-\prod_{i=0}^{N-1}\cos^2x_i\|)(\sum_{i=0}^{N-1}x_i^2(i+1))^{-\frac{1}{2}}`$</div>
Schaffer 2<sup>[11]</sup> | ![](pics/schaffer.jpg) | Highly multimodal, with symmetrical ripples that progressivly increase in magnitude closer to the origin. It's defined only for 2 dimensions.<br><div align="center">$`f(x)=0.5 + \frac{\sin(\sqrt(x_0^2+x_1^2))^2 - 0.5}{(1.0 + 0.001(x_0^2+x_1^2))^2}`$</div>
Himmelblau<sup>[8]</sup> | ![](pics/himmelblau.jpg) | Multimodal, with the four local optima sharing the same shallow basin. It's defined only for 2 dimensions.<br><div align="center">$`f(x)=(x_0^2+x_1-11)^2+(x_0+x_1^2-7)^2`$</div>
Pits and Holes<sup>[8]</sup> | ![](pics/pits_and_holes.jpg) | Multimodal. Designed to have multiple convex local optima well isolated, with different score and different attraction basin size.<br><div align="center">$`f_{\mu,C,v}(x)=-\sum_{i=0}^{N-1}N_{PDF}(x,\mu_i,C_i)v_i`$</div>

## Expanding the Library
A library like this one can never truly be considered complete. New useful functions are devised on a regular basis and new optima for already known functions can always be found.
For this reason, this library has been designed to be easily expanded. Aside from its definition, all the information about every function is saved in a separate Json file that can be easily editable. 
### Adding new Functions
If you are interested in adding a function to the library either open an issue ticket or send me an email. In order to include a function the following information are required:

- The name of the function;
- Its definition. It must come in the form of a python function that accepts a point (as a list of values) and returns a single floating value. In order to keep this library as portable as possible external libraries can not be used. Exceptions to this rule are libreries that come with any standard python installation (e.g. math) and numpy. This library is specifically focused on deterministic benchmark function, so no random operators can be used in the definition. 
- The number of dimensions where the function is defined. Most functions are defined for an arbitrary large dimensionality, on the other hand some functions restrict their scope to only a few dimensions. 
- Suggested boundaries. Normally the boundaries are the same (with a proper extrusion) for any number of dimensions. However, the library accept different boundaries according the value of a user-defined parameter (check the Json file for the Griewank function for an example);
- One or more known local minima. As a convention, all the functions of this library are designed for simulating a minimisation problem. Your function must have at least one known local minimum for at least one dimension.

Optionally you are free to send me a reference to the paper where the function first was discussed. It will be added to the function information.
### Suggesting a New Local Minimum
If you think that you have found a local minima that isn't listed in the function when *getLocalMinima* is called, you can let me know by opening a ticket or sending me an email.
A convenience function to assess a candidate point to be a local minimum is present for all the functions included. 
If you have a candidate local minimum $`x`$ for a function $`f`$ you can call the following function to validate it:
```python
fun.testLocalMinimum(x)
```
It returns a tuple *(response, message)* where *response* is a boolean and, if it is False, you'll find in the message some details on why the candidate point is not considered a local minimum.
It is important to note that this check is just an approximation. What is done here is sampling the surrounding region of $`x`$ and check if for all the sampled points $`f(y)>f(x)`$ holds.
The *validateLocalMinima* function accept two optional parameters:

- *radius_factor* is the maximum local radius of the sampling, scaled according the suggested boundaries (set as $`10^{-70}`$ by default);
- *n_tests* the number of random samplings performed (set as $`10^{5}`$ by default);

Invalid candidate minima can be mistakenly accepted if the *radius_factor* is too high. For example, check this snippet:
```python
In [1]: fun=bf.Hypersphere(n_dimensions=3)                                                                               
In [2]: point = fun.getMinimum()                                                                                       
In [3]: point
Out [3]: (0.0, [0.0, 0.0, 0.0])
In [4]: fun.testLocalMinimum(point[1][:-1]+[1e-71]) # false positive                             
Out[4]: (True, 'Point [0.0, 0.0, 1e-71] is a local minimum for Hypersphere!')
In [5]: fun.testLocalMinimum(point[1][:-1]+[1e-70]) # true negative
Out[5]: 
(False,
 'Point [-5.27227672e-71 -2.74251760e-73  3.25779003e-71] has a distance of 8.558916357655049e-71 from the candidate point [0.0, 0.0, 1e-71] and it has a lower value than it (3.8410849846089904e-141<=1e-140)')
In [6]: fun.testLocalMinimum(point[1][:-1]+[1e-71], radius_factor=1e-71) # true negative
Out[6]: 
(False,
 'Point [-1.32739337e-72 -3.36356596e-72  8.22706510e-72] has a distance of 4.027263002723288e-72 from the candidate point [0.0, 0.0, 1e-71] and it has a lower value than it (8.076014922727307e-143<=9.999999999999999e-143)')
```
To be accepted, a candidate point must be validated at least with the default values, but you are free to test your candidate point for stricker parameters (i.e. lower *radius_factor*, higher *n_tests*). Feel free to open a ticket with:

- The name of the function.
- The new minimum point.
- The *radius_factor* and *n_tests* values you used to validate it.

Some functions artificially create a large number of deceptive local minima (e.g. Ackley) with the declared purpose of making the search of the local optima harder. Those deceptive local minima are not interesting for this purpose, so they must not be considered.
### Function Info Specifications
Each function available in this library has a JSON file with the same name under the directory *functions_info* which contains all the metadata. Generally speaking, anything that is not the definition of the function goes in that file. Suggested boundaries, known minima and maxima at different dimensions and other information are stored there and loaded upon request.


## References

- [1]: Vanaret C., Gotteland J-B., Durand N., Alliot J-M. (2014) [Certified Global Minima for a Benchmark of Difficult Optimization Problems](https://hal-enac.archives-ouvertes.fr/hal-00996713/document). Technical report. Ecole Nationale de l'Aviation Civile. Toulouse, France
- [2]: Schwefel, H.-P.: Numerical optimization of computer models. Chichester: Wiley & Sons, 1981
- [3]: Pohlheim, H. [GEATbx Examples: Examples of Objective Functions](http://www.geatbx.com/download/GEATbx_ObjFunExpl_v37.pdf) 
- [4]: Dixon, L. C. W., & Szego, G. P. (1978). The global optimization problem: an introduction. Towards global optimization, 2, 1-15
- [5]: Molga, M., & Smutnicki, C. [Test functions for optimization needs](http://www.zsd.ict.pwr.wroc.pl/files/docs/functions.pdf) 
- [6]: Picheny, V., Wagner, T., & Ginsbourger, D. (2012). A benchmark of kriging-based infill criteria for noisy optimization.
- [7]: Adorio, E. P., & Diliman, U. P. [MVF - Multivariate Test Functions Library in C for Unconstrained Global Optimization](http://http://www.geocities.ws/eadorio/mvf.pdf)
- [8]: Himmelblau, D. (1972). Applied Nonlinear Programming. McGraw-Hill. ISBN 0-07-028921-2
- [9]: Ackley, D. H. (1987) "A connectionist machine for genetic hillclimbing", Kluwer Academic Publishers, Boston MA
- [10]:  C. J. Chung, R. G. Reynolds, “CAEP: An Evolution-Based Tool for Real-Valued Function Optimization Using Cultural Algorithms,” International Journal on Artificial Intelligence Tool, vol. 7, no. 3, pp. 239-291, 1998.
- [11]: Mishra, Sudhanshu K. "Some new test functions for global optimization and performance of repulsive particle swarm method." Available at SSRN 926132 (2006).
- [12]: De Jong, Kenneth Alan. "An analysis of the behavior of a class of genetic adaptive systems". University of Michigan, 1975.
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