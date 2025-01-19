import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import random

# Configuration parameters
CONFIG = {
    'initial_speed': 1,     # points per second
    'min_speed': 1,         # minimum points per second
    'max_speed': 10000,     # maximum points per second (100x more)
    'speed_step': 1,        # base increment (will scale with speed)
    'total_frames': 10000,
    'frame_rate': 50        # frames per second (50fps = 20ms interval)
}

# Animation control variables
animation_running = True
current_speed = CONFIG['initial_speed']

# Add point accumulator
point_accumulator = 0.0

# Define the vertices of the initial equilateral triangle
A = np.array([0.5, np.sqrt(0.75)])
B = np.array([0, 0])
C = np.array([1, 0])
vertices = [A, B, C]

points = []

# Generate a random starting point inside the triangle using convex combination
u = np.random.uniform(0, 1)
v = np.random.uniform(0, 1)
if u + v > 1:
    u, v = 1 - u, 1 - v
starting_point = (1 - u - v) * A + u * B + v * C

# Create two figures: one for animation, one for status
fig_anim = plt.figure('Animation')
fig_status = plt.figure('Status', figsize=(3, 2))
ax_anim = fig_anim.add_subplot(111)
ax_status = fig_status.add_subplot(111)

# Set up the animation plot
ax_anim.set_aspect('equal')
ax_anim.set_xlim(-0.1, 1.1)
ax_anim.set_ylim(-0.1, 1.1)

# Set up the status window
ax_status.axis('off')
status_text = ax_status.text(0.05, 0.5, '', transform=ax_status.transAxes)
help_text = """Controls:
SPACE - Pause/Resume
↑ - Increase speed
↓ - Decrease speed"""
help_box = ax_anim.text(0.98, 0.98, help_text, transform=ax_anim.transAxes,
                       verticalalignment='top', horizontalalignment='right',
                       bbox=dict(facecolor='white', alpha=0.8, edgecolor='gray', pad=5),
                       zorder=10)

def update_status_text():
    status = f'Status:\nPoints per second: {current_speed}\nSpeed multiplier: {current_speed/CONFIG["initial_speed"]}x\n{"Running" if animation_running else "Paused"}'
    status_text.set_text(status)
    fig_status.canvas.draw_idle()

def cleanup(event=None):
    """Close all windows and clean up resources"""
    plt.close('all')
    
def on_window_close(event):
    """Handle window close event"""
    cleanup()
    plt.close('all')  # Ensure all windows are closed

def on_key_press(event):
    global animation_running, current_speed
    
    if event.key == ' ':
        animation_running = not animation_running
    elif event.key == 'up':
        # Exponential speed increase
        speed_multiplier = max(1, current_speed // 10)
        current_speed = min(CONFIG['max_speed'], 
                          current_speed + CONFIG['speed_step'] * speed_multiplier)
    elif event.key == 'down':
        # Exponential speed decrease
        speed_multiplier = max(1, current_speed // 10)
        current_speed = max(CONFIG['min_speed'], 
                          current_speed - CONFIG['speed_step'] * speed_multiplier)
    
    update_status_text()

# Initialize plots for the current point, line to vertex, and trajectory
point_plot, = ax_anim.plot([], [], 'ro')  
line_plot, = ax_anim.plot([], [], 'b-')   
scatter_plot, = ax_anim.plot([], [], 'g.') 

# Plot the initial triangle
triangle = ax_anim.plot([A[0], B[0], C[0], A[0]], [A[1], B[1], C[1], A[1]])

current_point = starting_point.copy()

def init():
    # Initialize the plots
    point_plot.set_data([], [])
    line_plot.set_data([], [])
    scatter_plot.set_data([], [])
    return point_plot, line_plot

def update(frame):
    if not animation_running:
        return point_plot, line_plot, scatter_plot
    
    try:
        global current_point, points, point_accumulator
        
        # Accumulate points based on speed and frame rate
        point_accumulator += current_speed / CONFIG['frame_rate']
        points_to_add = int(point_accumulator)
        point_accumulator -= points_to_add
        
        # Add points
        for _ in range(points_to_add):
            next_vertex = random.choice(vertices)
            current_point = (current_point + next_vertex) / 2 
            points.append(current_point)
        
        # Update plots
        point_plot.set_data([current_point[0]], [current_point[1]])
        if points:
            point_x, point_y = zip(*points)
            scatter_plot.set_data(point_x, point_y)
        
        update_status_text()
        return point_plot, line_plot, scatter_plot
    except Exception as e:
        print(f"Update error: {e}")
        return point_plot, line_plot, scatter_plot

# Setup the animation
frames = np.arange(CONFIG['total_frames'])
anim = FuncAnimation(fig_anim, update, frames=frames, init_func=init, 
                    interval=20, blit=True)

# Connect events to both figures
fig_anim.canvas.mpl_connect('key_press_event', on_key_press)
fig_status.canvas.mpl_connect('key_press_event', on_key_press)
fig_anim.canvas.mpl_connect('close_event', on_window_close)
fig_status.canvas.mpl_connect('close_event', on_window_close)

# Initial status update
update_status_text()

try:
    plt.show()
except Exception as e:
    print(f"Display error: {e}")
    cleanup()