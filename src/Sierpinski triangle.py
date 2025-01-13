import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import random

A = np.array([0.5, np.sqrt(0.75)])
B = np.array([0, 0])
C = np.array([1, 0])
vertices = [A, B, C]

points = []

u = np.random.uniform(0, 1)
v = np.random.uniform(0, 1)
if u + v > 1:
    u, v = 1 - u, 1 - v
starting_point = (1 - u - v) * A + u * B + v * C # Kombinacja wypukła


fig, ax = plt.subplots()


point_plot, = ax.plot([], [], 'ro', label="Current Point")
line_plot, = ax.plot([], [], 'b-', label="Line to Vertex")
scatter_plot, = ax.plot([], [], 'g.', label="Trajectory") 

triangle = ax.plot([A[0], B[0], C[0], A[0]], [A[1], B[1], C[1], A[1]])

current_point = starting_point.copy()

def init():
    point_plot.set_data([], [])
    line_plot.set_data([], [])
    scatter_plot.set_data([], [])
    return point_plot, line_plot


def update(frame):
    global current_point
    next_vertex = random.choice(vertices)
    
    point_plot.set_data(current_point[0], current_point[1])
    line_plot.set_data([current_point[0], next_vertex[0]], [current_point[1], next_vertex[1]])
    
    current_point = (current_point + next_vertex)/2 
    points.append(current_point)
    point_x, point_y = zip(*points)
    scatter_plot.set_data(point_x, point_y)
    
    return point_plot, line_plot, scatter_plot

frames = np.arange(1000)

anim = FuncAnimation(fig, update, frames=frames, init_func=init, blit=True)


plt.show()