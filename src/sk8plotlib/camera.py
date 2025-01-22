import numpy as np
from .skater import Skater


class Camera:
    def __init__(
        self,
        fig,
        ax,
        skater: Skater,
        starting_scale: int = 100,
        scale: int = 10,
        velocity_zoom_response: float = 0.1,
        zoom_response: float = 0.025,
        max_camera_distance: float = 25,
        move_response: float = 1.5,
    ):
        self.fig, self.ax, self.skater = fig, ax, skater
        self.scale = starting_scale
        self.position = skater.position
        self.desired_scale = scale
        self.desired_position = skater.position

        self.scale_response = velocity_zoom_response
        self.minimum_scale = scale
        self.maximum_scale = starting_scale
        self.zoom_response = zoom_response

        self.max_camera_distance = max_camera_distance
        self.move_response = move_response

    def move_camera(self):
        self._update_scale()
        self._update_position()
        self.ax.set(
            xlim=(self.position[0] - self.scale, self.position[0] + self.scale),
            ylim=(self.position[1] - self.scale, self.position[1] + self.scale),
        )

    def _update_position(self):
        # We always aim to center on the skater, plus some velocity tolerance. We don't
        # let this get too big to try and stop the skater going off screen
        position_offset = self.skater.velocity * 0.3
        position_offset_magnitude = np.linalg.norm(position_offset)
        if position_offset_magnitude > self.max_camera_distance:
            position_offset *= self.max_camera_distance / position_offset_magnitude
        self.desired_position = self.skater.position + position_offset

        # BUT, we lag behind it.
        # We start by computing the difference between camera & skater
        difference = self.desired_position - self.position
        distance = np.linalg.norm(difference)

        # The amount that we move the camera scales on a few things
        # If the distance is greater than our max distance, always move closer than that
        amount_to_move = distance / self.max_camera_distance

        # Otherwise, we use a smooth scaling rule
        # if distance < self.max_camera_distance:
        amount_to_move = amount_to_move**self.move_response

        self.position += difference * amount_to_move

    def _update_scale(self):
        velocity = self.skater.velocity
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
            (self.desired_scale - self.scale) * self.zoom_response,
            -np.inf,
            self.zoom_response,
        )
        self.scale = np.clip(
            self.scale + scale_change, self.minimum_scale, self.maximum_scale
        )

        self.skater.set_marker_scale(self.minimum_scale / self.scale)
