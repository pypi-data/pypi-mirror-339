# pyillustrator

**pyillustrator** is a modular Python package designed for creating beautiful and configurable matplotlib subplot grids — perfect for creating aligned and aesthetic scientific figures, especially for publications.

---

## Features

- Golden, square, equal or custom aspect ratios
- Fine control over subplot spacing, margins, and grid layout
- Double-axis plotting with horizontal or vertical pairs
- Centralized configuration system
- LaTeX-friendly and publication-ready styling

---

## Installation

To install it from the repository you can install it
```
git clone https://github.com/yourusername/pyillustrator.git
cd pyillustrator
pip install .
```

PyPi installation is also available:
```
pip install pyillustrator
```

---

## Project Structure

```
pyillustrator/
├── __init__.py 
├── source/
│   ├── __init__.py         # Module exports
│   ├── plots.py            # Core plotting functions
│   ├── config.py           # Default settings and aspect ratio constants
│   └── utils.py            # Axes formatting and layout utilities
```

## Usage

Basic grid plot

```
from pyillustrator import grid_plot

fig, axs = grid_plot(2, 2)
axs[0,0].plot([0,1], [0,1])
```

Double grid (e.g., for comparison)

```
from pyillustrator import grid_plot_double

fig, axs = grid_plot_double(1, 2, pair='Horizontal')
axs[0,0,0].plot(...)  # Left half
axs[0,0,1].plot(...)  # Right half
```

Custom configuration

```
from pyillustrator import DEFAULT_CONFIG, grid_plot

config = DEFAULT_CONFIG.copy()
config["figwidth"] = 20
config["aspect"] = "Equal"
config["style"] = "seaborn"

fig, axs = grid_plot(2, 2, config)
```

---

## License

This project is licensed under the MIT License. See the LICENSE file for details.

---