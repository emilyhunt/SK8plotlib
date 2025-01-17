import numpy as np
import shapely
from shapely.geometry import LineString, Point, MultiPoint
from .variables import TIMESTEP, GRAVITY, TERMINAL_VELOCITY


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
    (-1, 0)
]


class Skater:
    def __init__(self, fig, ax, line_data):
        self.fig = fig
        self.ax = ax

        # Position & velocity
        self.x = 0.0
        self.y = 0.0
        self.v_x = 1.0
        self.v_y = 0.0

        # Run setup
        self.initialize_line_data(line_data)
        self.draw()

    def initialize_line_data(self, line_data):
        self.lines = [LineString(line) for line in line_data]

    def draw(self):
        self.points = self.ax.scatter(
            [self.x], [self.y], color="k", marker=_skater_points, linewidths=2.5, s=500
        )

    def update(self):
        x = self.x
        y = self.y
        v_x, v_y = self._apply_gravity()
        self._try_to_move(x, y, v_x, v_y)
        self._update_points()

    def _try_to_move(self, x, y, v_x, v_y, timestep=TIMESTEP):
        attempt = 0
        while attempt < 5:
            new_x, new_y = x + v_x * TIMESTEP, y + v_y * TIMESTEP

            collision, collision_time = self._check_for_collision(
                x, y, new_x, new_y, timestep
            )

            if not collision:
                self.x, self.y, self.v_x, self.v_y = new_x, new_y, v_x, v_y
                return

            x, y, v_x, v_y = self._handle_collision(collision, collision_time, v_x, v_y)
            timestep = timestep - collision_time
            attempt += 1

        self.x, self.y, self.v_x, self.v_y = new_x, new_y, v_x, v_y

    def _apply_gravity(self):
        v_x = np.clip(self.v_x, -TERMINAL_VELOCITY, TERMINAL_VELOCITY)
        v_y = np.clip(
            self.v_y - GRAVITY * TIMESTEP, -TERMINAL_VELOCITY, TERMINAL_VELOCITY
        )
        return v_x, v_y

    def _check_for_collision(self, old_x, old_y, new_x, new_y, timestep: float):
        line = LineString([(old_x, old_y), (new_x, new_y)])
        collisions = [
            big_line.intersection(line) for i, big_line in enumerate(self.lines)
        ]
        collisions = {
            i: collision
            for i, collision in enumerate(collisions)
            if not isinstance(collision, LineString)
        }
        if collisions:
            return self._select_best_collision(collisions, line, timestep)
        return None, None

    def _handle_collision(
        self, collision: dict[int, Point], collision_time: float, v_x, v_y
    ):
        SCALE = 0.01
        line_index = list(collision.keys())[0]
        line_collided = self.lines[line_index]
        collision_point = collision[line_index]

        # Set x/y at the collision
        x, y = collision_point.x, collision_point.y

        # Find normal vector of the surface
        # Todo needs to be scaled eventually
        distance = line_collided.line_locate_point(collision_point)
        point_1, point_2 = (
            line_collided.line_interpolate_point(distance - SCALE),
            line_collided.line_interpolate_point(distance + SCALE),
        )

        normal = np.asarray((-(point_2.y - point_1.y), (point_2.x - point_1.x)))
        normal = normal / np.sqrt(np.sum(normal**2))
        velocity = np.asarray((v_x, v_y))

        # Convert into motion along the slope
        undesired_motion = normal * np.dot(normal, velocity)
        desired_motion = velocity - undesired_motion
        # unit_vector_desired = desired_motion / np.sqrt(np.sum(desired_motion**2))
        output_motion = desired_motion  # unit_vector_desired * np.sqrt(np.sum(velocity**2))

        # Change velocity to be parallel
        v_x, v_y = output_motion[0], output_motion[1]
        return x, y + 0.05, v_x, v_y

    def _select_best_collision(
        self,
        collisions: dict[int, Point | MultiPoint],
        line: LineString,
        timestep: float,
    ):
        if len(collisions) > 1:
            raise NotImplementedError(
                "Unable to deal with multiple collisions at this time!"
            )  # todo

        collision_index = list(collisions.keys())[0]
        collision = collisions[collision_index]
        if isinstance(collision, MultiPoint):
            origin = Point(line.coords[0])
            distances = [point.distance(origin) for point in collision.geoms]
            index_smallest = np.argmin(distances)
            collision = collision.geoms[index_smallest]
            collisions[collision_index] = collision

        length_along_collision = shapely.line_locate_point(line, collision)
        time_elapsed = length_along_collision / line.length * timestep
        return collisions, time_elapsed

    def _update_points(self):
        self.points.set(offsets=[[self.x, self.y]])
