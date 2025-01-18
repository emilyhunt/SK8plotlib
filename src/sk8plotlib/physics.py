from sk8plotlib.input import UserInput
from sk8plotlib.variables import (
    GRAVITY,
    TERMINAL_VELOCITY,
    USER_ACCELERATION,
    USER_MAX_SPEED,
    USER_ROTATION_RATE,
)
import numpy as np
import shapely
from shapely.geometry import LineString, MultiPoint, Point


def _project_vector_along_plane(normal, vector, lossless=False):
    """Projects a vector along (i.e. parallel to) a plane.

    If smoothed, vector has same output magnitude as at input (good for sliding)
    """
    new_vector = vector - np.dot(normal, vector) * normal
    if lossless:
        denominator = np.linalg.norm(new_vector)
        if denominator != 0:
            new_vector *= np.linalg.norm(vector) / np.linalg.norm(new_vector)
    return new_vector


def _cap_velocity_to_terminal_velocity(velocity):
    total_velocity = np.linalg.norm(velocity)
    if total_velocity > TERMINAL_VELOCITY:
        velocity *= TERMINAL_VELOCITY / total_velocity
    return velocity


class PhysicsPoint:
    def __init__(
        self,
        x_start: float,
        y_start: float,
        line_data: list[np.ndarray],
        input: UserInput,
        v_x_start: float = 0.0,
        v_y_start: float = 0.0,
        rotation_start: float = 0.0,
    ):
        """Class representing a point in space that can collide with things."""
        self.position = np.asarray([x_start, y_start])
        self.velocity = np.asarray([v_x_start, v_y_start])
        self.lines = [LineString(line) for line in line_data]
        self.collided_line_id: int | None = None
        self.collided_line_point: Point | None = None
        self.input = input
        self.rotation = rotation_start

    def step(self, timestep):
        """Step the point one time."""
        if self.collided_line_id is None:
            self.move_in_air(timestep)
        else:
            self.move_on_surface(timestep, initial_move=True)

    def move_in_air(self, timestep):
        """Try to move the point through the air. If we hit something, then we move on
        the surface instead.
        """
        self.rotation += self._get_user_rotation(timestep)
        new_velocity = self.velocity + self._get_gravity_vector(timestep)

        self.validate_move(timestep, new_velocity)

    def move_on_surface(self, timestep, initial_move=False):
        normal = self._get_normal_vector_with_line()
        new_velocity = _project_vector_along_plane(normal, self.velocity, lossless=True)
        gravity = self._get_gravity_vector(timestep)
        new_velocity += _project_vector_along_plane(normal, gravity)
        if initial_move and np.linalg.norm(new_velocity) < USER_MAX_SPEED:
            user_contribution = self._get_user_vector(timestep)
            new_velocity += _project_vector_along_plane(
                normal, user_contribution, lossless=True
            )

        self.validate_move(timestep, new_velocity)

    def validate_move(self, timestep, new_velocity):
        # Cap to terminal velocity
        new_velocity = _cap_velocity_to_terminal_velocity(new_velocity)

        # Calc new position
        new_position = self.position + timestep * new_velocity

        # Look for collision
        was_on_surface_already = self.collided_line_id is not None
        collision, remaining_time = self.check_for_collision(
            new_position, self.position, timestep
        )
        if not collision:
            self.position, self.velocity = new_position, new_velocity
            if was_on_surface_already:
                self.check_if_still_on_surface()
            return

        # Keep moving on surface if we did collide
        self.handle_collision(new_velocity, was_on_surface_already)
        self.move_on_surface(remaining_time)

    def check_for_collision(self, new_position, old_position, timestep):
        line = LineString([old_position, new_position])

        # Find all times we passed through a line
        collisions = [big_line.intersection(line) for big_line in self.lines]
        collisions = {
            i: collision
            for i, collision in enumerate(collisions)
            if not isinstance(collision, LineString)
        }
        if not collisions:
            self.collided_line_id, self.collided_line_point = None, None
            return False, 0.0

        # Select the first time it happened
        self.collided_line_id, self.collided_line_point = self._select_best_collision(
            collisions, line
        )

        # Stop here if user doesn't want timestep calculations
        if timestep == 0.0:
            return True, 0.0

        # Calculate how long it took to happen
        length_along_collision = shapely.line_locate_point(
            line, self.collided_line_point
        )
        time_elapsed = length_along_collision / line.length * timestep
        return True, time_elapsed

    def _select_best_collision(
        self,
        collisions: dict[int, Point | MultiPoint],
        path_moved: LineString,
    ):
        if len(collisions) > 1:
            raise NotImplementedError(
                "Unable to deal with multiple colliding lines at this time!"
            )  # todo

        collision_index = list(collisions.keys())[0]
        collision = collisions[collision_index]
        if isinstance(collision, MultiPoint):
            origin = Point(path_moved.coords[0])
            distances = [point.distance(origin) for point in collision.geoms]
            index_smallest = np.argmin(distances)
            collision = collision.geoms[index_smallest]
        return collision_index, collision

    def handle_collision(self, new_velocity, collision_should_be_lossless):
        normal = self._get_normal_vector_with_line()
        self.velocity = _project_vector_along_plane(
            normal, new_velocity, lossless=collision_should_be_lossless
        )
        # Todo handle scale on the up-y amount
        self.position = np.asarray(
            [self.collided_line_point.x, self.collided_line_point.y + 0.05]
        )

    def check_if_still_on_surface(self):
        """Checks upto some amount below to see if the line is still there. If not,
        then we consider the skateboard airborne.
        """
        test_position = self.position.copy()
        test_position[1] -= 0.25  # Todo set this programmatically
        on_surface = self.check_for_collision(test_position, self.position, 0.0)[0]
        # Todo optionally also stick to the surface - not sure if good idea or not tbh
        if on_surface:
            self.rotate_to_surface()

    def rotate_to_surface(self):
        normal = self._get_normal_vector_with_line()  # Todo cache for next time
        self.rotation = np.arctan2(-normal[0], normal[1]) * 0.66

    def rotate_from_user_input(self, timestep):
        self.rotation -= self._get_user_rotation(timestep)

    def _get_gravity_vector(self, timestep=1.0):
        return np.asarray([0, -GRAVITY * timestep])

    def _get_user_vector(self, timestep):
        return np.asarray(
            [self.input.left_right_input() * USER_ACCELERATION * timestep, 0]
        )

    def _get_user_rotation(self, timestep):
        return self.input.up_down_input() * timestep * USER_ROTATION_RATE

    def _get_normal_vector_with_line(
        self,
    ):
        if self.collided_line_point is None:
            raise RuntimeError(
                "Cannot calculate normal vector as collided_line_point not set."
            )
        if self.collided_line_id is None:
            raise RuntimeError(
                "Cannot calculate normal vector as collided_line_id not set."
            )
        line_collided = self.lines[self.collided_line_id]

        # Todo needs to be scaled properly eventually
        SCALE = 0.0001
        distance = line_collided.line_locate_point(self.collided_line_point)
        point_1, point_2 = (
            line_collided.line_interpolate_point(distance - SCALE),
            line_collided.line_interpolate_point(distance + SCALE),
        )
        normal = np.asarray((-(point_2.y - point_1.y), (point_2.x - point_1.x)))
        normal = normal / np.linalg.norm(normal)
        return normal
