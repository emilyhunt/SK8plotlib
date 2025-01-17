import numpy as np


class Camera:
    def __init__(self, fig, ax, skater):
        self.fig, self.ax, self.skater = fig, ax, skater

    def move_camera(self):
        SCALE = 10

        x, y, v_x, v_y = self.skater.x, self.skater.y, self.skater.v_x, self.skater.v_y
        location, velocity = np.asarray([x, y]), np.asarray([v_x, v_y])

        location += velocity * 0.05

        self.ax.set(
            xlim=(location[0] - SCALE, location[0] + SCALE),
            ylim=(location[1] - SCALE, location[1] + SCALE),
        )
