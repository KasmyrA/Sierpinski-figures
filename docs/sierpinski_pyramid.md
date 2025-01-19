# 3D Sierpinski Pyramid

The Sierpinski Pyramid, also known as the Sierpinski Tetrahedron, is a 3D fractal formed by recursively subdividing a tetrahedron into smaller tetrahedrons.

## Implementation

The implementation uses the midpoint displacement method to generate the points of the Sierpinski Pyramid.

### Example Usage

```python
from sierpinski.shapes_3d import SierpinskiPyramid

# Create a pyramid with 4 iterations
pyramid = SierpinskiPyramid(iterations=4)
fig = pyramid.plot_3d()
fig.show()  # Opens interactive 3D visualization
fig.write_html("pyramid.html")  # Save as interactive HTML
```

### Visualization

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

### Mathematical Background

The Sierpinski Pyramid is constructed by recursively removing the central tetrahedron from each subdivided tetrahedron. This process continues indefinitely, creating a self-similar fractal pattern.
