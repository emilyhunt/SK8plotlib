import numpy as np


class Camera:
    def __init__(
        self,
        fig,
        ax,
        skater,
        starting_scale=100,
        scale=10,
        scale_response=0.1,
        zoom_response=0.05,
    ):
        self.fig, self.ax, self.skater = fig, ax, skater
        self.scale = starting_scale
        self.desired_scale = scale
        self.scale_response = scale_response
        self.minimum_scale = scale
        self.zoom_response = zoom_response

    def move_camera(self):
        x, y, v_x, v_y = self.skater.x, self.skater.y, self.skater.v_x, self.skater.v_y
        location, velocity = np.asarray([x, y]), np.asarray([v_x, v_y])

        location += velocity * 0.05

        self.ax.set(
            xlim=(location[0] - self.scale, location[0] + self.scale),
            ylim=(location[1] - self.scale, location[1] + self.scale),
        )
        self._update_scale(velocity)

    def _update_scale(self, velocity):
        excess_velocity = np.linalg.norm(velocity) - 1
        if excess_velocity > 10:
            self.desired_scale = np.clip(
                self.minimum_scale + excess_velocity * self.scale_response,
                self.minimum_scale,
                self.minimum_scale * 2.0,
            )
        else:
            self.desired_scale = self.minimum_scale

        scale_change = np.clip(
            (self.desired_scale - self.scale) * self.zoom_response, -np.inf, self.zoom_response
        )
        self.scale += scale_change

        self.skater.set_marker_scale(self.minimum_scale / self.scale)
