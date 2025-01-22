import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

class InvarianceVisualizer:
    def __init__(self):
        self.vertices = np.array([[0, 0], [1, 0], [0.5, 0.866]])
        self.points = []
        self.current_point = np.random.rand(2)
        
        self.fig, self.ax = plt.subplots(figsize=(8, 8))
        self.scatter = self.ax.scatter([], [], c='blue', alpha=0.3, s=1)
        self.ax.set_facecolor('white')  # White background
        
    def step(self):
        vertex = self.vertices[np.random.randint(3)]
        self.current_point = (self.current_point + vertex) / 2
        self.points.append(self.current_point)
        
    def update(self, frame):
        for _ in range(10):  # Add 10 points per frame
            self.step()
        points_array = np.array(self.points)
        self.scatter.set_offsets(points_array)
        return self.scatter,
    
    def animate(self):
        self.ax.set_xlim(-0.1, 1.1)
        self.ax.set_ylim(-0.1, 1.0)
        self.ax.scatter(self.vertices[:, 0], self.vertices[:, 1], 
                       c='red', s=50, label='Vertices')  # Make vertices more visible
        self.ax.set_title("Lemma 1: Invariance Property Visualization")
        self.ax.grid(True, alpha=0.2)  # Add light grid
        self.ax.legend()  # Add legend
        
        anim = FuncAnimation(self.fig, self.update, frames=100, 
                           interval=50, blit=True)
        plt.show()

if __name__ == "__main__":
    viz = InvarianceVisualizer()
    viz.animate()
