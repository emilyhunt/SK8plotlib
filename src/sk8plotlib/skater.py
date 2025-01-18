from sk8plotlib.physics import PhysicsPoint
from matplotlib.markers import MarkerStyle
from matplotlib.transforms import Affine2D
from .input import UserInput
import numpy as np


_skater_points = [
    (-1, -0.25),
    (-1, 0),
    (-1.5, 0),
    (-1.5, 0.1),
    (1.5, 0.1),
    (1.5, 0.0),
    (1.0, 0.0),
    (1.0, -0.25),
    (1.0, 0.0),
    (-1, 0),
    (-1, -0.25),
    (-1, 0),
]


class Skater:
    def __init__(self, fig, ax, line_data, input: UserInput):
        self.fig = fig
        self.ax = ax
        # self.input = input
        self.physics = PhysicsPoint(0.0, 5.0, line_data, input)
        self.marker_scale = 1.0

        # Run setup
        self.draw()

    @property
    def x(self):
        return self.physics.position[0]

    @property
    def y(self):
        return self.physics.position[1]

    @property
    def v_x(self):
        return self.physics.velocity[0]

    @property
    def v_y(self):
        return self.physics.velocity[1]

    @property
    def rotation(self):
        return self.physics.rotation

    def draw(self):
        self.marker = MarkerStyle(
            _skater_points, transform=Affine2D().translate(0, 0.2)
        )
        self.points = self.ax.scatter(
            [self.x], [self.y], color="k", marker=self.marker, linewidths=2.5, s=500
        )

    def update(self, timestep):
        self.physics.step(timestep)
        self._update_points()

    def set_marker_scale(self, scale):
        self.marker_scale = scale

    def _update_points(self):
        self.points.set(
            offsets=[[self.x, self.y]],
            transform=Affine2D().rotate(self.rotation).scale(self.marker_scale),
        )
