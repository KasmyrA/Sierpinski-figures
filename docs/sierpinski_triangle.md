# 2D Sierpinski Triangle

The Sierpinski Triangle is a fractal that is formed by recursively subdividing an equilateral triangle into smaller equilateral triangles.

## Implementation

The implementation uses the midpoint displacement method to generate the points of the Sierpinski Triangle.

### Example Usage

```python
from sierpinski.shapes_2d import SierpinskiTriangle

# Create a triangle with 6 iterations
triangle = SierpinskiTriangle(iterations=6)
fig = triangle.plot()
fig.show()  # Opens in browser or notebook
fig.write_html("triangle.html")  # Save as interactive HTML
```

### Visualization

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

### Mathematical Background

The Sierpinski Triangle is constructed by recursively removing the central triangle from each subdivided triangle. This process continues indefinitely, creating a self-similar fractal pattern.
