# Sierpinski Figures

A Python implementation for generating and visualizing Sierpinski figures in 2D and 3D spaces. This project was developed as part of the Mathematical Modeling course.

## Overview

This project provides tools for creating and visualizing various Sierpinski fractals, including:
- Sierpinski Triangle (2D)
- Sierpinski Carpet (2D)
- Sierpinski Pyramid (3D)
- Sierpinski Sponge (3D)

## Features

- Generation of Sierpinski fractals with customizable iteration depth
- 2D visualization using matplotlib
- 3D rendering with interactive rotation and zoom capabilities
- Efficient recursive implementation
- Support for saving generated figures as images

## Requirements

- Python 3.12+
- Poetry (Python package manager)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/sierpinski-figures.git
cd sierpinski-figures
```

2. Install Poetry (if not already installed):
```bash
curl -sSL https://install.python-poetry.org | python3 -
```
Or

```bask
pip install poetry
```
3. Install project dependencies:
```bash
poetry install
```

4. Activate the virtual environment:
```bash
poetry shell
```

## Project Dependencies

Main dependencies managed by Poetry:
- numpy: Mathematical operations and array handling
- plotly: Interactive visualization of 2D and 3D figures
- pandas: Data manipulation and structuring

## Usage

### 2D Sierpinski Triangle

```python
from sierpinski.shapes_2d import SierpinskiTriangle

# Create a triangle with 6 iterations
triangle = SierpinskiTriangle(iterations=6)
fig = triangle.plot()
fig.show()  # Opens in browser or notebook
fig.write_html("triangle.html")  # Save as interactive HTML
```

### 3D Sierpinski Pyramid

```python
from sierpinski.shapes_3d import SierpinskiPyramid

# Create a pyramid with 4 iterations
pyramid = SierpinskiPyramid(iterations=4)
fig = pyramid.plot_3d()
fig.show()  # Opens interactive 3D visualization
fig.write_html("pyramid.html")  # Save as interactive HTML
```

### Features of Plotly Visualization

Egz:
- Interactive 3D rotation and zoom
- Hover information showing coordinates
- Export to HTML for interactive web viewing
- Multiple color schemes and styling options
- Camera position control
- Screenshot capabilities

## Project Structure

```
sierpinski-figures/
├── sierpinski/
│   ├── __init__.py
│   ├── shapes_2d.py
│   ├── shapes_3d.py
│   └── utils.py
├── examples/
│   ├── 2d_examples.py
│   └── 3d_examples.py
├── tests/
├── pyproject.toml    # Poetry configuration and dependencies
├── poetry.lock      # Lock file for reproducible installations
└── README.md
```

## Mathematical Background

The Sierpinski figures are fractal sets that exhibit self-similarity at different scales. The project implements these mathematical concepts:

- Recursive subdivision of geometric shapes
- Fractal dimension calculations
- Iterative geometric transformations

## Contributing

This is a semester project for Mathematical Modeling course. Feel free to use this code for educational purposes.

## License

[Choose appropriate license]

## Authors

[Authors]

Mathematical Modeling Course

Silesian University of Science

