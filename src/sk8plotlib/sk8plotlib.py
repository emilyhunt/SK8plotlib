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
        fig, animator.update_animation, frames=range(100), interval=MIN_TIMESTEP
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
        self.last_frame_time = None
        self.average_timestep = MIN_TIMESTEP

    def update_animation(self, frame):
        this_frame = time.time()
        if self.last_frame_time is None:
            self.last_frame_time = this_frame - MIN_TIMESTEP
        
        timestep = this_frame - self.last_frame_time
        # self.skater.update(np.clip(self.average_timestep, MIN_TIMESTEP, 2*MIN_TIMESTEP))
        self.skater.update(MIN_TIMESTEP)
        self.camera.move_camera()

        # Framerate cap - calculated from a 1 second moving average
        self.average_timestep = (
            self.average_timestep * (MAX_FRAMERATE - 1) / MAX_FRAMERATE
            + timestep * 1 / MAX_FRAMERATE
        )
        # if self.average_timestep < MIN_TIMESTEP:
        #     time.sleep(MIN_TIMESTEP - self.average_timestep)
        print(f"FPS (av): {1 / self.average_timestep:.2f} | FPS: {1 / timestep:.2f}")

        self.last_frame_time = this_frame
