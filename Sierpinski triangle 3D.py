import numpy as np
import plotly.graph_objects as go
import random

SPEED = 30 # durationof one frame in ms
POINTS_NUM = 500 # number of points

A = np.array([0.5, np.sqrt(0.75), 0])
B = np.array([0, 0, 0])
C = np.array([1, 0, 0])
D = np.array([0.5, (1/6)*np.sqrt(3), np.sqrt(2)/np.sqrt(3)])
vertices = [A, B, C, D]

starting_point = [0.4, 0.4, 0.2]
middle_point = starting_point.copy()

points = [starting_point] # saves coordinates of subsequent points
frames = [] # saves subsequent frames

for frame_num in range(2*POINTS_NUM): 
    next_vertex = random.choice(vertices) # random vertex
    current_point = middle_point # the middle point becomes the current point
    middle_point = (current_point + next_vertex) / 2 # calculates middle of the line between vertex and current point (new middle point)
    points.append(current_point)
    x, y, z = zip(*points)

    frames.append(go.Frame(data=[ # frame without middle point
        go.Scatter3d(x=x, y=y, z=z, mode='markers', marker=dict(size=2, color='blue')),  # all previous points
        go.Scatter3d(x=[current_point[0]], y=[current_point[1]], z=[current_point[2]], mode='markers', marker=dict(size=4, color='red')), # current point
        go.Scatter3d(x=[], y=[], z=[], mode='markers', marker=dict(size=4, color='yellow')), # middle point (not visible)
        go.Scatter3d(x=[next_vertex[0], x[-1]], y=[next_vertex[1], y[-1]], z=[next_vertex[2], z[-1]], mode="lines", line=dict(color='black')), # line
        go.Mesh3d(x=[A[0], B[0], C[0], D[0]], y=[A[1], B[1], C[1], D[1]], z=[A[2], B[2], C[2], D[2]], color='lightpink', opacity=0.2) # tertrahedron
    ]))

    frames.append(go.Frame(data=[ # frame with middle point
        go.Scatter3d(x=x, y=y, z=z, mode='markers', marker=dict(size=2, color='blue')),   # all previous points
        go.Scatter3d(x=[current_point[0]], y=[current_point[1]], z=[current_point[2]], mode='markers', marker=dict(size=4, color='red')), # current point
        go.Scatter3d(x=[middle_point[0]], y=[middle_point[1]], z=[middle_point[2]], mode='markers', marker=dict(size=4, color='yellow')), # middle point
        go.Scatter3d(x=[next_vertex[0], x[-1]], y=[next_vertex[1], y[-1]], z=[next_vertex[2], z[-1]], mode="lines", line=dict(color='black')), # line
        go.Mesh3d(x=[A[0], B[0], C[0], D[0]], y=[A[1], B[1], C[1], D[1]], z=[A[2], B[2], C[2], D[2]], color='lightpink', opacity=0.2) # tertrahedron
    ]))

layout = go.Layout(
    scene=dict(xaxis=dict(range=[-0.1, 1.1], title="X"), yaxis=dict(range=[-0.1, 1.1], title="Y"), zaxis=dict(range=[-0.1, 1.1], title="Z")),
    showlegend=False,
    updatemenus=[dict(type="buttons", showactive=False, buttons=[dict(label="Play", method="animate", args=[None, dict(frame=dict(duration=SPEED, redraw=True), fromcurrent=True)])])]
    )



fig = go.Figure( # initial view
    data=[
        go.Scatter3d(x=[starting_point[0]], y=[starting_point[1]], z=[starting_point[2]], mode='markers', marker=dict(size=4, color='red')),  # starting point
        go.Scatter3d(x=[], y=[], z=[], mode='markers', marker=dict(size=2, color='red')), # not visible
        go.Scatter3d(x=[], y=[], z=[], mode='markers', marker=dict(size=4, color='yellow')),
        go.Scatter3d(x=[], y=[], z=[], mode="lines", line=dict(color='black')),
        go.Mesh3d(x=[A[0], B[0], C[0], D[0]], y=[A[1], B[1], C[1], D[1]], z=[A[2], B[2], C[2], D[2]], color='lightpink', opacity=0.2) # tertrahedron
    ],
    layout=layout,
    frames=frames
    )

fig.show()
