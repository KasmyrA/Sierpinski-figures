import numpy as np
import plotly.graph_objects as go
import random

SPEED = 30  # Duration of one frame in ms
POINTS_NUM = 500  # Number of points

# Define the vertices of the initial tetrahedron
A = np.array([0.5, np.sqrt(0.75), 0])
B = np.array([0, 0, 0])
C = np.array([1, 0, 0])
D = np.array([0.5, (1/6)*np.sqrt(3), np.sqrt(2)/np.sqrt(3)])
vertices = [A, B, C, D]

starting_point = [0.4, 0.4, 0.2]
middle_point = starting_point.copy()

points = [starting_point]  # Saves coordinates of subsequent points
frames = []  # Saves subsequent frames

for frame_num in range(2 * POINTS_NUM): 
    next_vertex = random.choice(vertices)  # Random vertex
    current_point = middle_point  # The middle point becomes the current point
    middle_point = (current_point + next_vertex) / 2  # Calculate the midpoint
    points.append(current_point)
    x, y, z = zip(*points)

    # Create frames for the animation
    frames.append(go.Frame(data=[
        go.Scatter3d(x=x, y=y, z=z, mode='markers', marker=dict(size=2, color='blue')),  # All previous points
        go.Scatter3d(x=[current_point[0]], y=[current_point[1]], z=[current_point[2]], mode='markers', marker=dict(size=4, color='red')),  # Current point
        go.Scatter3d(x=[], y=[], z=[], mode='markers', marker=dict(size=4, color='yellow')),  # Middle point (not visible)
        go.Scatter3d(x=[next_vertex[0], x[-1]], y=[next_vertex[1], y[-1]], z=[next_vertex[2], z[-1]], mode="lines", line=dict(color='black')),  # Line
        go.Mesh3d(x=[A[0], B[0], C[0], D[0]], y=[A[1], B[1], C[1], D[1]], z=[A[2], B[2], C[2], D[2]], color='lightpink', opacity=0.2)  # Tetrahedron
    ]))

    frames.append(go.Frame(data=[
        go.Scatter3d(x=x, y=y, z=z, mode='markers', marker=dict(size=2, color='blue')),  # All previous points
        go.Scatter3d(x=[current_point[0]], y=[current_point[1]], z=[current_point[2]], mode='markers', marker=dict(size=4, color='red')),  # Current point
        go.Scatter3d(x=[middle_point[0]], y=[middle_point[1]], z=[middle_point[2]], mode='markers', marker=dict(size=4, color='yellow')),  # Middle point
        go.Scatter3d(x=[next_vertex[0], x[-1]], y=[next_vertex[1], y[-1]], z=[next_vertex[2], z[-1]], mode="lines", line=dict(color='black')),  # Line
        go.Mesh3d(x=[A[0], B[0], C[0], D[0]], y=[A[1], B[1], C[1], D[1]], z=[A[2], B[2], C[2], D[2]], color='lightpink', opacity=0.2)  # Tetrahedron
    ]))

layout = go.Layout(
    scene=dict(xaxis=dict(range=[-0.1, 1.1], title="X"), yaxis=dict(range=[-0.1, 1.1], title="Y"), zaxis=dict(range=[-0.1, 1.1], title="Z")),
    showlegend=False,
    updatemenus=[dict(type="buttons", showactive=False, buttons=[dict(label="Play", method="animate", args=[None, dict(frame=dict(duration=SPEED, redraw=True), fromcurrent=True)])])]
)

fig = go.Figure(
    data=[
        go.Scatter3d(x=[starting_point[0]], y=[starting_point[1]], z=[starting_point[2]], mode='markers', marker=dict(size=4, color='red')),  # Starting point
        go.Scatter3d(x=[], y=[], z=[], mode='markers', marker=dict(size=2, color='red')),  # Not visible
        go.Scatter3d(x=[], y=[], z=[], mode='markers', marker=dict(size=4, color='yellow')),
        go.Scatter3d(x=[], y=[], z=[], mode="lines", line=dict(color='black')),
        go.Mesh3d(x=[A[0], B[0], C[0], D[0]], y=[A[1], B[1], C[1], D[1]], z=[A[2], B[2], C[2], D[2]], color='lightpink', opacity=0.2)  # Tetrahedron
    ],
    layout=layout,
    frames=frames
)

fig.show()
