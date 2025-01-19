import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from dataclasses import dataclass
from typing import List, Tuple, Optional
import random
from numpy.typing import NDArray
import time  # Add time import

@dataclass
class Config:
    initial_speed: float = 1.0
    min_speed: float = 1.0
    max_speed: float = 100000.0
    speed_step: float = 1.0
    total_frames: int = 10000
    frame_rate: int = 120  # Changed from 50 to 120
    idle_frame_rate: int = 120  # New setting for idle state
    max_points: int = 500000  # Increased maximum points
    trim_threshold: float = 0.8  # Keep 80% of points when trimming
    window_title: str = "Sierpinski Triangle Generator"
    status_window_title: str = "Status and Controls"
    initial_point_size: float = 3.0  # Changed from 1.0 to 3.0
    min_point_size: float = 0.1
    max_point_size: float = 5.0
    point_size_step: float = 0.1
    # Add color configuration
    current_point_color: str = 'red'
    triangle_color: str = 'blue'
    points_color: str = 'green'
    # Add performance settings
    batch_size: int = 1000  # Process points in batches
    # Add triangle configuration
    triangle_vertices: List[Tuple[float, float]] = None
    max_display_points: int = 100000  # Maximum points to display at once
    display_downsampling: float = 0.5  # Fraction of points to show when exceeding limit

    def __post_init__(self):
        if self.triangle_vertices is None:
            # Default equilateral triangle
            self.triangle_vertices = [
                (0.5, np.sqrt(0.75)),  # A
                (0.0, 0.0),            # B
                (1.0, 0.0)             # C
            ]

class SierpinskiTriangle:
    def _setup_windows(self):
        """Initialize and configure windows"""
        self.fig_anim = plt.figure(self.config.window_title)
        self.fig_status = plt.figure(self.config.status_window_title, figsize=(3, 2))
        self.ax_anim = self.fig_anim.add_subplot(111)
        self.ax_status = self.fig_status.add_subplot(111)
        
        # Configure animation window
        self.ax_anim.set_aspect('equal')
        self.ax_anim.set_xlim(-0.1, 1.1)
        self.ax_anim.set_ylim(-0.1, 1.1)
        
        # Configure status window
        self.ax_status.axis('off')
        self._setup_text()

    def _setup_plots(self):
        """Initialize all plots"""
        self.point_plot, = self.ax_anim.plot([], [], 'o', 
            color=self.config.current_point_color, markersize=self.point_size)
        self.line_plot, = self.ax_anim.plot([], [], '-',
            color=self.config.triangle_color)
        self.scatter_plot, = self.ax_anim.plot([], [], '.',
            color=self.config.points_color, markersize=self.point_size)
        
        # Plot the initial triangle
        self.triangle = self.ax_anim.plot(
            [self.A[0], self.B[0], self.C[0], self.A[0]],
            [self.A[1], self.B[1], self.C[1], self.A[1]],
            color=self.config.triangle_color
        )

    def _connect_events(self):
        """Connect all event handlers"""
        self.fig_anim.canvas.mpl_connect('key_press_event', self._on_key_press)
        self.fig_status.canvas.mpl_connect('key_press_event', self._on_key_press)
        self.fig_anim.canvas.mpl_connect('close_event', self._on_close)
        self.fig_status.canvas.mpl_connect('close_event', self._on_close)
        
        # Setup animation
        self.anim = FuncAnimation(
            self.fig_anim, 
            self._update_animation,
            frames=np.arange(self.config.total_frames),
            init_func=self._init_animation,
            interval=1000//self.config.idle_frame_rate,  # Use idle frame rate
            blit=True
        )

    def __init__(self, config: Config):
        """Initialize the Sierpinski Triangle generator"""
        self.config = config
        self.animation_running = True
        self.current_speed = config.initial_speed
        self.point_size = config.initial_point_size
        self.point_accumulator = 0.0
        self.total_points_generated = 0  # Add total points counter
        self.last_frame_time = time.time()
        self.fps = self.config.frame_rate
        
        # Initialize vertices from config
        self.A = np.array(config.triangle_vertices[0])
        self.B = np.array(config.triangle_vertices[1])
        self.C = np.array(config.triangle_vertices[2])
        self.vertices = [self.A, self.B, self.C]
        self.points = np.zeros((0, 2))  # Store points as NumPy array
        self.display_points = np.zeros((0, 2))  # Buffer for displayed points
        
        # Initialize starting point
        u, v = random.uniform(0, 1), random.uniform(0, 1)
        if u + v > 1:
            u, v = 1 - u, 1 - v
        self.current_point = (1 - u - v) * self.A + u * self.B + v * self.C
        
        # Setup components in correct order
        self._setup_windows()
        self._setup_plots()
        self._connect_events()
        self.update_status_text()  # Initial status update

    def _setup_text(self):
        """Setup status and help text"""
        self.status_text = self.ax_status.text(0.05, 0.5, '', transform=self.ax_status.transAxes)
        help_text = """Controls:
SPACE  Pause/Resume
↑/↓  Change speed
+/-  Change point size
R    Reset"""
        self.help_box = self.ax_anim.text(0.98, 0.98, help_text, 
                                         transform=self.ax_anim.transAxes,
                                         verticalalignment='top', 
                                         horizontalalignment='right',
                                         bbox=dict(facecolor='white', alpha=0.8, 
                                                 edgecolor='gray', pad=5),
                                         zorder=10)

    def _init_animation(self):
        """Initialize animation"""
        self.point_plot.set_data([], [])
        self.line_plot.set_data([], [])
        self.scatter_plot.set_data([], [])
        return self.point_plot, self.line_plot

    def _update_display_points(self):
        """Update display buffer with downsampled points if needed"""
        if len(self.points) > self.config.max_display_points:
            # Randomly sample points for display
            display_size = int(self.config.max_display_points * self.config.display_downsampling)
            indices = np.random.choice(len(self.points), display_size, replace=False)
            self.display_points = self.points[indices]
        else:
            self.display_points = self.points

    def update_status_text(self):
        """Update status window text"""
        current_time = time.time()
        frame_time = current_time - self.last_frame_time
        self.last_frame_time = current_time
        
        # Smooth FPS calculation with moving average
        if frame_time > 0:
            current_fps = 1.0 / frame_time
            self.fps = 0.9 * self.fps + 0.1 * current_fps  # Smoothing factor
        
        status = (f'Status:\nPoints per second: {self.current_speed}\n'
                 f'Speed multiplier: {self.current_speed/self.config.initial_speed:.1f}x\n'
                 f'Point size: {self.point_size:.1f}\n'
                 f'Visible points: {len(self.points):,}\n'
                 f'Total generated: {self.total_points_generated:,}\n'
                 f'FPS: {self.fps:.1f}\n'
                 f'{"Running" if self.animation_running else "Paused"}')
        self.status_text.set_text(status)
        self.fig_status.canvas.draw_idle()

    def _on_key_press(self, event):
        """Handle key press events"""
        if event.key == ' ':
            self.animation_running = not self.animation_running
        elif event.key == 'up':
            speed_multiplier = max(1, self.current_speed // 10)
            self.current_speed = min(self.config.max_speed, 
                                   self.current_speed + self.config.speed_step * speed_multiplier)
        elif event.key == 'down':
            speed_multiplier = max(1, self.current_speed // 10)
            self.current_speed = max(self.config.min_speed, 
                                   self.current_speed - self.config.speed_step * speed_multiplier)
        elif event.key in ['=', '+']:  # Handle both = and + keys
            self.point_size = min(self.config.max_point_size,
                                self.point_size + self.config.point_size_step)
            self._update_point_size()
        elif event.key in ['-', '_']:  # Handle both - and _ keys
            self.point_size = max(self.config.min_point_size,
                                self.point_size - self.config.point_size_step)
            self._update_point_size()
        elif event.key == 'r':  # Add reset functionality
            self.points = np.zeros((0, 2))
            self.display_points = np.zeros((0, 2))
            self.total_points_generated = 0
            u, v = random.uniform(0, 1), random.uniform(0, 1)
            if u + v > 1:
                u, v = 1 - u, 1 - v
            self.current_point = (1 - u - v) * self.A + u * self.B + v * self.C
        
        self.update_status_text()

    def _update_point_size(self):
        """Update the size of points in all plots"""
        self.point_plot.set_markersize(self.point_size * 3)  # Make current point more visible
        self.scatter_plot.set_markersize(self.point_size)
        self.fig_anim.canvas.draw_idle()  # Force redraw

    def _is_point_valid(self, point: NDArray) -> bool:
        """Check if point is within valid bounds"""
        x, y = point
        # Check if point is within reasonable bounds
        return (-0.1 <= x <= 1.1) and (-0.1 <= y <= 1.1)

    def _generate_next_point(self, current: NDArray) -> NDArray:
        """Generate next point with validation"""
        for _ in range(5):  # Try a few times if point is invalid
            next_vertex = random.choice(self.vertices)
            new_point = (current + next_vertex) / 2
            if self._is_point_valid(new_point):
                return new_point
        # If all attempts fail, project point back into triangle
        return self._project_to_triangle(current)

    def _project_to_triangle(self, point: NDArray) -> NDArray:
        """Project point back into triangle if it's outside"""
        # Calculate barycentric coordinates
        v0 = self.B - self.A
        v1 = self.C - self.A
        v2 = point - self.A
        
        d00 = np.dot(v0, v0)
        d01 = np.dot(v0, v1)
        d11 = np.dot(v1, v1)
        d20 = np.dot(v2, v0)
        d21 = np.dot(v2, v1)
        
        denom = d00 * d11 - d01 * d01
        v = (d11 * d20 - d01 * d21) / denom
        w = (d00 * d21 - d01 * d20) / denom
        u = 1.0 - v - w
        
        # Clamp coordinates to ensure point is inside triangle
        v = np.clip(v, 0, 1)
        w = np.clip(w, 0, 1)
        u = np.clip(u, 0, 1)
        
        # Normalize
        total = u + v + w
        u, v, w = u/total, v/total, w/total
        
        # Return projected point
        return u * self.A + v * self.B + w * self.C

    def _update_animation(self, frame):
        """Update animation frame"""
        if not self.animation_running:
            return self.point_plot, self.line_plot, self.scatter_plot

        try:
            # Stop adding points if we reached the maximum
            if len(self.points) >= self.config.max_points:
                self.animation_running = False
                print(f"Reached maximum points ({self.config.max_points:,}). Animation stopped.")
                self.update_status_text()
                return self.point_plot, self.line_plot, self.scatter_plot

            self.point_accumulator += self.current_speed / self.config.frame_rate
            points_to_add = int(self.point_accumulator)
            self.point_accumulator -= points_to_add

            if points_to_add > 0:
                # Limit points_to_add to not exceed max_points
                points_to_add = min(points_to_add, self.config.max_points - len(self.points))
                if points_to_add <= 0:
                    return self.point_plot, self.line_plot, self.scatter_plot

                # Pre-allocate array for new points
                new_points = np.zeros((points_to_add, 2))
                
                for i in range(points_to_add):
                    self.current_point = self._generate_next_point(self.current_point)
                    new_points[i] = self.current_point
                    self.total_points_generated += 1

                # Efficiently concatenate arrays
                self.points = np.vstack((self.points, new_points))
                self._update_display_points()
                self._update_plots()
                self.update_status_text()

            return self.point_plot, self.line_plot, self.scatter_plot
        except Exception as e:
            print(f"Update error: {e}")
            return self.point_plot, self.line_plot, self.scatter_plot

    # Remove _manage_points_memory since we don't need it anymore
    def _manage_points_memory(self):
        """Manage points list to prevent memory overflow"""
        pass  # No longer needed as we stop at max points

    def _update_plots(self):
        """Update all plot data"""
        self.point_plot.set_data([self.current_point[0]], [self.current_point[1]])
        if len(self.display_points) > 0:
            self.scatter_plot.set_data(self.display_points[:, 0], self.display_points[:, 1])
            self.point_plot.set_markersize(self.point_size * 3)
            self.scatter_plot.set_markersize(self.point_size)

    def _on_close(self, event):
        """Handle window close event"""
        plt.close('all')

    def run(self):
        """Start the animation"""
        try:
            plt.show()
        except Exception as e:
            print(f"Display error: {e}")
        finally:
            plt.close('all')

# Create and run the application
if __name__ == "__main__":
    config = Config()
    triangle = SierpinskiTriangle(config)
    triangle.run()