[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.8373435.svg)](https://doi.org/10.5281/zenodo.8373435)

# useful-math-functions

`useful-math-functions` is a collection of useful mathematical functions with a
focus on:

1. **ease of use** - the functions are designed to be as easy to use as possible
2. **pure python** - the functions are written in much python as possible and
   only use external libraries when necessary
3. **documentation** - the functions are documented in code itself with:
   1. Examples
   2. Equations
   3. References
   4. Links to external resources

## Installation

The package can be installed via pip:

```bash
pip install useful-math-functions
```

and for Visualizations:

```bash
# matplotlib
pip install useful-math-functions[matplotlib]

# plotly
pip install useful-math-functions[plotly]

# all visualizations
pip install useful-math-functions[all]
```

## Usage

The package can be imported like any other python package:

```python
from umf.core.create import OptBench
res = OptBench(["DeJongN5Function"], dim=3)
res.plot_type_3d = "plot_surface"
res.plot()
res.save_as_image()
```

![_](https://github.com/Anselmoo/useful-math-functions/blob/main/docs/extra/images/DeJongN5Function.png?raw=true)

To use the newly added functions:

```python
from umf.functions.optimization.special import HimmelblauFunction
import numpy as np

x = np.linspace(-5, 5, 100)
y = np.linspace(-5, 5, 100)
X, Y = np.meshgrid(x, y)
Z = HimmelblauFunction(X, Y).__eval__

import matplotlib.pyplot as plt
fig = plt.figure()
ax = fig.add_subplot(111, projection="3d")
ax.plot_surface(X, Y, Z, cmap="viridis")
plt.savefig("HimmelblauFunction.png", dpi=300, transparent=True)
```

```python
from umf.functions.optimization.valley_shaped import Rosenbrock2DFunction
import numpy as np

x = np.linspace(-2, 2, 100)
y = np.linspace(-1, 3, 100)
X, Y = np.meshgrid(x, y)
Z = RosenbrockFunction(X, Y).__eval__

import matplotlib.pyplot as plt
fig = plt.figure()
ax = fig.add_subplot(111, projection="3d")
ax.plot_surface(X, Y, Z, cmap="viridis")
plt.savefig("RosenbrockFunction.png", dpi=300, transparent=True)
```

## Documentation

The documentation can be found
[here](https://anselmoo.github.io/useful-math-functions/).

## Contributing

Contributions are welcome. For major changes, please open an issue first to
discuss what you would like to change.

## License

The project is licensed under the
[MIT](https://github.com/Anselmoo/useful-math-functions/blob/main/LICENSE)
license.
