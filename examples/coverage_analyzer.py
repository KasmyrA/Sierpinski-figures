import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.patches import Circle, Polygon
from matplotlib.colors import LogNorm
from dataclasses import dataclass
from typing import List, Tuple, Optional
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class AnalyzerConfig:
    """Configuration for the coverage analyzer"""
    grid_size: int = 100
    buffer_size: int = 1000
    points_per_frame: int = 10
    animation_interval: int = 50
    epsilon: float = 0.01
    figure_size: Tuple[int, int] = (15, 5)

class CoverageAnalyzer:
    def __init__(self, config: Optional[AnalyzerConfig] = None):
        """Initialize the analyzer with optional configuration"""
        self.config = config or AnalyzerConfig()
        self.vertices: np.ndarray = np.array([[0, 0], [1, 0], [0.5, 0.866]])
        self.points: List[np.ndarray] = []
        self.current_point: np.ndarray = np.random.rand(2)
        self.target_point: np.ndarray = np.array([0.333, 0.289])
        self.found_points: List[np.ndarray] = []
        self.coverage_grid: np.ndarray = np.zeros(
            (self.config.grid_size, self.config.grid_size)
        )
        self.visits_near_target: List[int] = []
        self.total_iterations: int = 0
        
        # Precompute grid scaling factors
        self.grid_scale = (self.config.grid_size - 1) / 1.2  # -0.1 to 1.1 range

    def update_coverage(self, points: np.ndarray) -> None:
        """
        Update coverage grid with new points using vectorized operations
        
        Args:
            points: Array of 2D points
        """
        x = ((points[:, 0] + 0.1) * self.grid_scale).astype(int)
        y = ((points[:, 1] + 0.1) * self.grid_scale).astype(int)
        
        mask = (0 <= x) & (x < self.config.grid_size) & \
               (0 <= y) & (y < self.config.grid_size)
        
        np.add.at(self.coverage_grid, (y[mask], x[mask]), 1)

    def step(self) -> None:
        """Perform one iteration of the chaos game"""
        try:
            # Vectorized point generation
            vertices_batch = self.vertices[
                np.random.randint(3, size=self.config.points_per_frame)
            ]
            new_points = (self.current_point + vertices_batch) / 2
            
            for point in new_points:
                self.current_point = point
                self.points.append(point)
                self.total_iterations += 1
                
                if np.linalg.norm(point - self.target_point) < self.config.epsilon:
                    self.found_points.append(point)
                    
            self.visits_near_target.append(len(self.found_points))
            self.update_coverage(new_points)
            
        except Exception as e:
            logger.error(f"Error in step: {e}")
            raise

    def visualize(self) -> None:
        """Create and display the interactive visualization"""
        fig = plt.figure(figsize=self.config.figure_size)
        gs = plt.GridSpec(1, 3, figure=fig)
        ax1 = fig.add_subplot(gs[0])  # Points plot
        ax2 = fig.add_subplot(gs[1])  # Heatmap
        ax3 = fig.add_subplot(gs[2])  # Coverage progress
        
        # Setup main plot
        ax1.set_xlim(-0.1, 1.1)
        ax1.set_ylim(-0.1, 1.0)
        ax1.set_title("Point Distribution")
        
        # Draw triangle
        triangle = Polygon(self.vertices, fill=False, color='black')
        ax1.add_patch(triangle)
        
        # Target area
        target = ax1.scatter([self.target_point[0]], [self.target_point[1]], 
                           c='red', s=100, label='Target')
        epsilon_circle = Circle(self.target_point, self.config.epsilon, 
                             fill=False, color='red', linestyle='--')
        ax1.add_patch(epsilon_circle)
        points = ax1.scatter([], [], c='blue', alpha=0.1, s=1)
        found = ax1.scatter([], [], c='green', alpha=0.5, s=20, label='Found')
        ax1.legend()
        
        # Setup heatmap
        heatmap = ax2.imshow(np.zeros((self.config.grid_size, self.config.grid_size)), extent=[-0.1, 1.1, -0.1, 1.0],
                            cmap='viridis', norm=LogNorm(vmin=1, vmax=100))
        ax2.set_title("Coverage Density")
        plt.colorbar(heatmap, ax=ax2)
        
        # Setup progress plot
        ax3.set_xlim(0, 1000)
        ax3.set_ylim(0, 50)
        ax3.set_title("Points Found vs Iterations")
        ax3.set_xlabel("Iterations")
        ax3.set_ylabel("Points Found")
        progress_line, = ax3.plot([], [], 'b-')
        
        def update(frame):
            for _ in range(self.config.points_per_frame):
                self.step()
                
            # Update points plot
            points.set_offsets(self.points[-self.config.buffer_size:])  # Show last buffer_size points
            if self.found_points:
                found.set_offsets(self.found_points)
                
            # Update heatmap
            heatmap.set_array(self.coverage_grid)
            
            # Update progress
            progress_line.set_data(range(len(self.visits_near_target)), 
                                 self.visits_near_target)
            
            return points, found, heatmap, progress_line
        
        anim = FuncAnimation(fig, update, frames=None, interval=self.config.animation_interval, blit=True)
        plt.tight_layout()
        plt.show()

if __name__ == "__main__":
    try:
        # Custom configuration
        config = AnalyzerConfig(
            grid_size=120,
            buffer_size=1500,
            points_per_frame=15
        )
        analyzer = CoverageAnalyzer(config)
        analyzer.visualize()
    except Exception as e:
        logger.error(f"Application error: {e}")
