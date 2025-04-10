# Versions History

## v1.1.4

- refactored code a bit, added better description
- fixed https://gitlab.com/luca.baronti/python_benchmark_functions/-/issues/1

## v1.1.3

- fixed Schwefel function definition

## v1.1.2

- Added another function
- Made the abstract BenchmarkFunction public by removing the prepended underscore to make extension more streamlined

## v1.1.1

- Fixed an import bug
- Updated the README

## v1.1

- Updated the README
- Split functions_info.json file into several files in a directory with the same name; removed functions_info.json and changed the relative code
- Added function to validate a candidate local minimum
- Added optional custom boundaries in the show function
- Added simple minima grid search for all the functions
- Added simple minima random search for all the functions
- Added and verified local minima of De Jong 5 and De Jong 3
- Refractored API (most getter functions now have a simpler form)
- Refractored the JSON schema for the functions meta-info
- Added FunctionInfoWriter to facilitate the addition of newfound optima
- Show function now optionally accepts a list of points to show on the plot
- Changed heatmap colour to viridis for consistency reasons
- Added version to the functions info
- Added CI/CD directives

## v0.1.2

- Minor fixes
