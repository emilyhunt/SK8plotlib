import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.animation import FuncAnimation
from .variables import MAX_FRAMERATE, MIN_TIMESTEP
from .matplotlib_hacks import fetch_matplotlib_data
from .skater import Skater
from .camera import Camera
from .input import UserInput
import time

matplotlib.use("QtAgg")


def sk8plot(fig: Figure):
    animator = PlotAnimator(fig)
    animation = FuncAnimation(  # noqa: F841
        fig, animator.update_animation, frames=range(100), interval=0.0
    )
    plt.show()


class PlotAnimator:
    def __init__(self, fig):
        self.fig = fig
        self.ax, self.lines, self.line_data = fetch_matplotlib_data(fig)

        # Some beautification
        # fig.canvas.setWindowTitle("SK8plotlib - ollie on your data")
        # fig.suptitle("SK8plotlib - ollie on your data")
        fig.suptitle("SK8plotlib - grind your axles on your graphs", y=0.95)

        # Make components
        self.input = UserInput(self.fig)
        self.skater = Skater(self.fig, self.ax, self.line_data, self.input)
        self.camera = Camera(self.fig, self.ax, self.skater)
        self.camera.move_camera()
        self.render_time_start = None
        self.average_timestep = MIN_TIMESTEP

    def update_animation(self, frame):
        if self.render_time_start is None:
            self.render_time_start = time.time()

        self.skater.update(
            np.clip(self.average_timestep, MIN_TIMESTEP, 4 * MIN_TIMESTEP)
        )
        self.camera.move_camera()

        time_end = time.time()
        time_to_process_frame = time_end - self.render_time_start

        # Framerate cap - calculated from a 1 second moving average
        self.average_timestep = (
            self.average_timestep * (MAX_FRAMERATE - 1) / MAX_FRAMERATE
            + time_to_process_frame * 1 / MAX_FRAMERATE
        )
        sleep_time = 0.0
        if self.average_timestep < MIN_TIMESTEP:
            sleep_time = MIN_TIMESTEP - self.average_timestep
            time.sleep(sleep_time)
        print(
            f"FPS (av): {1 / (self.average_timestep + sleep_time):.2f} | FPS: {1 / (time_to_process_frame + sleep_time):.2f}"  # | av: {self.average_timestep:.3f}"
        )

        self.render_time_start = time.time()
