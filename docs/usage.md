# Usage Guide

## Quick Start

### Installation

This guide provides detailed instructions on how to use the Sierpinski Figures project to generate and visualize fractals.

## 2D Sierpinski Triangle

### Creating a Sierpinski Triangle

```python
from sierpinski.shapes_2d import SierpinskiTriangle

# Create a triangle with 6 iterations
triangle = SierpinskiTriangle(iterations=6)
fig = triangle.plot()
fig.show()  # Opens in browser or notebook
fig.write_html("triangle.html")  # Save as interactive HTML
```

### Visualizing the Triangle

The 2D Sierpinski Triangle is visualized using matplotlib. The points are plotted iteratively, and the process can be animated to show the formation of the fractal.

### Algorithm Explanation

1. **Vertices Definition**: The vertices of the initial equilateral triangle are defined as points `A`, `B`, and `C`.
2. **Starting Point**: A random starting point inside the triangle is generated using a convex combination of the vertices.
3. **Plot Initialization**: The initial triangle and plots for the current point, line to vertex, and trajectory are set up.
4. **Animation Initialization**: The `init` function initializes the plots.
5. **Update Function**: The `update` function is called for each frame of the animation. It:
   - Chooses a random vertex.
   - Updates the current point plot.
   - Updates the line plot to the chosen vertex.
   - Calculates the midpoint between the current point and the chosen vertex.
   - Updates the scatter plot with the trajectory.
6. **Animation Creation**: The `FuncAnimation` function creates the animation using the `update` function and the frames.

## 3D Sierpinski Pyramid

### Creating a Sierpinski Pyramid

```python
from sierpinski.shapes_3d import SierpinskiPyramid

# Create a pyramid with 4 iterations
pyramid = SierpinskiPyramid(iterations=4)
fig = pyramid.plot_3d()
fig.show()  # Opens interactive 3D visualization
fig.write_html("pyramid.html")  # Save as interactive HTML
```

### Visualizing the Pyramid

The 3D Sierpinski Pyramid is visualized using Plotly. The points are plotted iteratively, and the process can be animated to show the formation of the fractal.

### Algorithm Explanation

1. **Vertices Definition**: The vertices of the initial tetrahedron are defined as points `A`, `B`, `C`, and `D`.
2. **Starting Point**: A starting point inside the tetrahedron is defined.
3. **Plot Initialization**: The initial tetrahedron and plots for the current point, line to vertex, and trajectory are set up.
4. **Frame Generation**: For each frame:
   - A random vertex is chosen.
   - The current point is updated to the midpoint between the current point and the chosen vertex.
   - The points and frames are updated with the new current point and line to the vertex.
5. **Layout and Animation**: The layout for the 3D plot is defined, and the animation is created using Plotly's `go.Figure` and `go.Frame`.

## Additional Features

### Plotly Visualization

- Interactive 3D rotation and zoom
- Hover information showing coordinates
- Export to HTML for interactive web viewing
- Multiple color schemes and styling options
- Camera position control
- Screenshot capabilities

### Saving Figures

Both 2D and 3D figures can be saved as interactive HTML files using the `write_html` method. This allows you to share the visualizations easily.

### Customization

You can customize the appearance of the figures by modifying the parameters in the `plot` and `plot_3d` methods. This includes changing colors, sizes, and other styling options.
