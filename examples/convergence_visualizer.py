import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.patches import Polygon
from dataclasses import dataclass
from typing import List, Tuple, Optional
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class VisualizerConfig:
    """Configuration parameters for the visualizer"""
    points_per_frame: int = 5  # Reduced from 20
    max_points: int = 2000
    animation_interval: int = 100  # Increased from 50
    figure_size: Tuple[int, int] = (15, 6)
    rolling_window: int = 50  # Added rolling window parameter
    max_frames: int = 10000  # Add maximum frames limit
    theory_decay_rate: float = 15.0  # Adjusted theoretical decay rate

class ConvergenceVisualizer:
    def __init__(self, config: Optional[VisualizerConfig] = None):
        """Initialize the visualizer with optional configuration"""
        self.config = config or VisualizerConfig()
        self.vertices: np.ndarray = np.array([[0, 0], [1, 0], [0.5, 0.866]])
        self.point_off: np.ndarray = np.array([0.4, 0.4])
        self.points_off: List[np.ndarray] = [self.point_off]
        self.points_on: List[np.ndarray] = []
        self.distances: List[float] = []
        self.running: bool = True
        self.initial_distance = None  # Store initial distance for theoretical line
        self.frame_count: int = 0
        self.paused_text = None
        self.iteration_count: int = 0  # Add iteration counter
        self.points_generated: int = 1  # Replace total_points with points_generated
        self.points_count = 0  # New counter
        
        try:
            self.twin_point = self.find_twin_point(self.point_off)
            self.points_on = [self.twin_point]
        except Exception as e:
            logger.error(f"Failed to initialize twin point: {e}")
            raise
        
    def find_twin_point(self, point: np.ndarray) -> np.ndarray:
        """
        Find the closest point on the Sierpinski triangle.
        
        Args:
            point: 2D point coordinates
        Returns:
            Closest point on the triangle
        """
        # First check if point is inside triangle
        def point_in_triangle(pt, triangle):
            A, B, C = triangle
            v0, v1, v2 = C - A, B - A, pt - A
            dot00 = np.dot(v0, v0)
            dot01 = np.dot(v0, v1)
            dot02 = np.dot(v0, v2)
            dot11 = np.dot(v1, v1)
            dot12 = np.dot(v1, v2)
            inv_denom = 1 / (dot00 * dot11 - dot01 * dot01)
            u = (dot11 * dot02 - dot01 * dot12) * inv_denom
            v = (dot00 * dot12 - dot01 * dot02) * inv_denom
            return u >= 0 and v >= 0 and u + v <= 1

        if point_in_triangle(point, self.vertices):
            # Use midpoints of closest subdivision
            midpoints = (self.vertices + np.roll(self.vertices, -1, axis=0)) / 2
            all_points = np.vstack([self.vertices, midpoints])
            distances = np.linalg.norm(all_points - point, axis=1)
            return all_points[np.argmin(distances)]
        else:
            # Project onto nearest edge
            edges = np.array([self.vertices, np.roll(self.vertices, -1, axis=0)])
            proj_points = []
            for edge in edges:
                v = edge[1] - edge[0]
                t = max(0, min(1, np.dot(point - edge[0], v) / np.dot(v, v)))
                proj = edge[0] + t * v
                proj_points.append(proj)
            distances = [np.linalg.norm(p - point) for p in proj_points]
            return proj_points[np.argmin(distances)]

    def calculate_rolling_average(self, data: List[float], window: int) -> np.ndarray:
        """Calculate rolling average of distances"""
        if len(data) < window:
            return np.array(data)
        return np.convolve(data, np.ones(window)/window, mode='valid')

    def visualize(self) -> None:
        """Create and display the interactive visualization"""
        try:
            fig = plt.figure(figsize=self.config.figure_size)
            gs = plt.GridSpec(1, 2, figure=fig)
            ax1 = fig.add_subplot(gs[0])
            ax2 = fig.add_subplot(gs[1])
            
            # Setup main plot
            ax1.set_xlim(-0.1, 1.1)
            ax1.set_ylim(-0.1, 1.0)
            ax1.set_title("Convergence Visualization")
            ax1.grid(True, alpha=0.2)
            
            # Draw triangle
            triangle = Polygon(self.vertices, fill=False, color='black')
            ax1.add_patch(triangle)
            
            # Initialize plots
            path_off, = ax1.plot([], [], 'b-', alpha=0.5, label='Point path')
            path_on, = ax1.plot([], [], 'r--', alpha=0.5, label='Twin point path')
            point_off = ax1.scatter([], [], c='blue', s=100, label='Current point')
            point_on = ax1.scatter([], [], c='red', s=100, label='Twin point')
            ax1.legend()
            
            # Setup convergence plot
            ax2.set_xlim(0, self.config.max_points)
            ax2.set_ylim(1e-4, 1)  # Adjusted y-axis limits
            ax2.set_yscale('log')
            ax2.set_title("Distance Convergence")
            ax2.set_xlabel("Iterations")
            ax2.set_ylabel("Distance (log scale)")
            ax2.grid(True, which='major', linestyle='-', alpha=0.5)
            ax2.grid(True, which='minor', linestyle=':', alpha=0.2)
            
            dist_line, = ax2.plot([], [], 'b-', alpha=0.8, label='Actual (rolling avg)')
            theory_line, = ax2.plot([], [], 'r--', alpha=0.6, label='Theoretical (1/2ⁿ)')
            raw_line, = ax2.plot([], [], 'c.', alpha=0.3, markersize=1, label='Raw distances')
            ax2.legend(loc='upper right')

            # Add frame counter and pause indicator
            ax1.text(0.02, 0.98, '', transform=ax1.transAxes,
                    name='monospace', fontsize=10,
                    verticalalignment='top',
                    bbox=dict(facecolor='white', alpha=0.7),
                    zorder=100)
            
            # Add instruction text
            ax1.text(0.02, 0.02, 'Click anywhere to pause/resume',
                    transform=ax1.transAxes,
                    fontsize=8,
                    color='gray',
                    bbox=dict(facecolor='white', alpha=0.7))

            # Make pause text more visible
            self.paused_text = ax1.text(0.5, 0.5, 'PAUSED',
                                      transform=ax1.transAxes,
                                      horizontalalignment='center',
                                      verticalalignment='center',
                                      color='red',
                                      fontsize=20,
                                      bbox=dict(facecolor='white', alpha=0.8),
                                      visible=False)

            def update(frame):
                if not self.running:
                    self.paused_text.set_visible(True)
                    return path_off, path_on, point_off, point_on, dist_line, theory_line, raw_line, self.paused_text
                
                self.paused_text.set_visible(False)
                
                try:
                    vertices_batch = self.vertices[
                        np.random.randint(3, size=self.config.points_per_frame)
                    ]
                    new_points_off = (self.point_off + vertices_batch) / 2
                    new_points_on = (self.twin_point + vertices_batch) / 2
                    
                    # Process each new point
                    for new_off, new_on in zip(new_points_off, new_points_on):
                        self.point_off = new_off
                        self.twin_point = new_on
                        self.points_off.append(new_off.copy())
                        self.points_on.append(new_on.copy())
                        self.distances.append(np.linalg.norm(new_off - new_on))
                        self.points_count += 1  # Increment counter for each point
                        
                        if len(self.points_off) > self.config.max_points:
                            self.points_off.pop(0)
                            self.points_on.pop(0)
                            self.distances.pop(0)

                    # Update counter text with actual count
                    ax1.texts[0].set_text(f'Points: {self.points_count}')
                    
                    # Update plots
                    points_off = np.array(self.points_off)
                    points_on = np.array(self.points_on)
                    
                    path_off.set_data(points_off[:, 0], points_off[:, 1])
                    path_on.set_data(points_on[:, 0], points_on[:, 1])
                    point_off.set_offsets([self.point_off])
                    point_on.set_offsets([self.twin_point])
                    
                    # Store initial distance for theoretical line
                    if self.initial_distance is None and self.distances:
                        self.initial_distance = self.distances[0]

                    # Update convergence plot
                    x = np.arange(len(self.distances))
                    raw_line.set_data(x, self.distances)
                    
                    # Calculate and plot rolling average
                    if len(self.distances) > 3:
                        rolling_avg = self.calculate_rolling_average(
                            self.distances, 
                            self.config.rolling_window
                        )
                        x_rolling = np.arange(len(rolling_avg))
                        dist_line.set_data(x_rolling, rolling_avg)
                    
                    # Update theoretical line with improved decay rate
                    if self.initial_distance is not None:
                        theory = self.initial_distance * (0.5 ** (x/self.config.theory_decay_rate))
                        theory_line.set_data(x, theory)
                    
                    # Update points counter with total points
                    ax1.texts[0].set_text(f'Points generated: {self.points_generated}')
                    
                    # Check max points instead of iterations
                    if self.points_count >= self.config.max_frames:
                        self.running = False
                    
                    return path_off, path_on, point_off, point_on, dist_line, theory_line, raw_line, self.paused_text

                except Exception as e:
                    logger.error(f"Error in animation update: {e}")
                    self.running = False
                    return path_off, path_on, point_off, point_on, dist_line, theory_line, raw_line, self.paused_text

            def on_click(event):
                self.running = not self.running

            fig.canvas.mpl_connect('button_press_event', on_click)
            anim = FuncAnimation(fig, update, frames=None, interval=self.config.animation_interval, blit=True)
            plt.tight_layout()
            plt.show()

        except Exception as e:
            logger.error(f"Failed to create visualization: {e}")
            raise

if __name__ == "__main__":
    try:
        # Custom configuration
        config = VisualizerConfig(
            points_per_frame=1, 
            max_points=2000,
            animation_interval=100, 
            rolling_window=50,
            theory_decay_rate=15.0,
            max_frames=10000
        )
        viz = ConvergenceVisualizer(config)
        viz.visualize()
    except Exception as e:
        logger.error(f"Application error: {e}")
