import matplotlib.pyplot as plt
from matplotlib.figure import Figure
import matplotlib

from sk8plotlib.variables import FRAMERATE
from .matplotlib_hacks import fetch_matplotlib_data
from .skater import Skater
from .camera import Camera
from matplotlib.animation import FuncAnimation

matplotlib.use("QtAgg")


def sk8plot(fig: Figure):
    animator = PlotAnimator(fig)
    animation = FuncAnimation(
        fig, animator.update_animation, frames=range(100), interval=1000 / FRAMERATE
    )
    plt.show()


class PlotAnimator:
    def __init__(self, fig):
        self.fig = fig
        self.ax, self.lines, self.line_data = fetch_matplotlib_data(fig)

        # Some beautification
        fig.canvas.setWindowTitle("SK8plotlib - ollie on your data")
        fig.suptitle("SK8plotlib - ollie on your data")

        # Make components
        self.skater = Skater(self.fig, self.ax, self.line_data)
        self.camera = Camera(self.fig, self.ax, self.skater)
        self.camera.move_camera()

    def update_animation(self, frame):
        self.skater.update()
        self.camera.move_camera()
