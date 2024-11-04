from typing import List
from pygame import Surface
import pygame
from Geometry import Directions, Point, Rectangle, Vector
from drawing.utils import get_rectangle_corners


# change name
def tuples_list(point_list: List[Point]):
    """
    Convert list of points to list of tuples
    """
    return [(p.x, p.y) for p in point_list]


class SideMirrors:
    """
    Class responsible for drawing side mirrors
    """

    def __init__(self, body: Rectangle, screen: Surface, color: str = "black"):
        self.screen = screen
        self.color = color
        self.length = body.length / 20
        self.width = body.width / 8
        self.distance_to_front = body.length / 4

    def draw_mirror(self, start_point: Point, body: Rectangle, direction: Directions):
        width_vector = body.direction.get_orthogonal_vector(direction, self.width)
        length_vector = width_vector.get_orthogonal_vector(direction, self.length)
        corners_list = get_rectangle_corners(start_point, width_vector, length_vector)
        pygame.draw.polygon(self.screen, self.color, tuples_list(corners_list))

    def draw(self, body: Rectangle):
        mirror_position_vector = body.direction.get_negative_of_a_vector().scale_to_len(
            self.distance_to_front
        )
        self.draw_mirror(
            body.front_left.copy().add_vector(mirror_position_vector),
            body,
            Directions.LEFT,
        )
        self.draw_mirror(
            body.front_right.copy().add_vector(mirror_position_vector),
            body,
            Directions.RIGHT,
        )


class FrontLights:
    """
    Class responsible for drawing front lights
    """

    def __init__(self, body: Rectangle, screen: Surface, color: str = "yellow"):
        self.screen = screen
        self.color = color
        self.length = body.length / 15
        self.width = body.width / 4

    def draw_light(self, start_point: Point, body: Rectangle, direction: Directions):
        width_vector = body.direction.get_orthogonal_vector(direction, self.width)
        length_vector = width_vector.get_orthogonal_vector(direction, self.length)
        corners_list = get_rectangle_corners(start_point, width_vector, length_vector)
        pygame.draw.polygon(self.screen, self.color, tuples_list(corners_list))

    def draw(self, body: Rectangle):
        self.draw_light(body.front_left.copy(), body, Directions.RIGHT)
        self.draw_light(body.front_right.copy(), body, Directions.LEFT)


class Wheels:
    """
    Class responsible for drawing front wheels
    """

    def __init__(self, body: Rectangle, screen: Surface, color: str = "#262626"):
        self.screen = screen
        self.color = color
        self.length = body.length / 4
        self.width = body.width / 8

    def draw_wheel(
        self, start_point: Point, body: Rectangle, direction: Directions, angle: float
    ):
        width_vector = body.direction.get_orthogonal_vector(direction, self.width)
        length_vector = width_vector.get_orthogonal_vector(direction, self.length)
        corners_list = get_rectangle_corners(start_point, width_vector, length_vector)
        rotation_point_vector = Vector(corners_list[2], corners_list[0]).scale(0.5)
        rotation_point = start_point.copy().add_vector(rotation_point_vector)
        rotated_corners = [
            corner.rotate_over_point(rotation_point, angle) for corner in corners_list
        ]
        pygame.draw.polygon(self.screen, self.color, tuples_list(rotated_corners))

    def draw(self, body: Rectangle):
        self.draw_wheel(body.front_left.copy(), body, Directions.RIGHT)
        self.draw_wheel(body.front_right.copy(), body, Directions.LEFT)


class BasicBrandDrafter:
    """
    Class responsible for drawing basic brand car on the screen
    """

    def __init__(self, width: float, length: float, color: str):
        """
        Initialize the drafter of basic brand cars

        :param width: width of the car
        :param length: length of the car
        :param color: color of the car
        """
        self.width = width
        self.length = length
        self.color = color

    def draw_front_window(self):
        pts = [Point(0, 0) for i in range(4)]

        length_vec = Vector(self.front_left, self.front_right).orthogonal_vector(
            self.length * 4 // 15, TurnDir.RIGHT
        )
        width_vec = Vector(self.rear_left, self.front_left).orthogonal_vector(
            self.width / 8, TurnDir.RIGHT
        )

        pts[0] = self.front_left.add_vector(length_vec).add_vector(width_vec)
        width_vec = Vector(self.rear_left, self.front_left).orthogonal_vector(
            self.width * 0.75, TurnDir.RIGHT
        )
        pts[1] = pts[0].add_vector(width_vec)

        length_vec = Vector(self.front_left, self.front_right).orthogonal_vector(
            self.length // 7, TurnDir.RIGHT
        )
        width_vec = Vector(self.rear_left, self.front_left).orthogonal_vector(
            self.width / 8, TurnDir.RIGHT
        )
        pts[3] = pts[0].add_vector(width_vec).add_vector(length_vec)
        width_vec = Vector(self.rear_left, self.front_left).orthogonal_vector(
            self.width // 2, TurnDir.RIGHT
        )
        pts[2] = pts[3].add_vector(width_vec)

        pygame.draw.polygon(self.screen, "black", tuples_list(pts))

    def draw_side_windows(self):
        pts_left = [Point(0, 0) for i in range(4)]
        pts_right = [Point(0, 0) for i in range(4)]

        length_vec = Vector(self.front_left, self.front_right).orthogonal_vector(
            self.length * 0.4, TurnDir.RIGHT
        )
        width_vec = Vector(self.rear_left, self.front_left).orthogonal_vector(
            self.width / 8, TurnDir.RIGHT
        )
        pts_left[0] = self.front_left.add_vector(length_vec).add_vector(width_vec)

        width_vec = Vector(self.rear_left, self.front_left).orthogonal_vector(
            self.width / 8, TurnDir.LEFT
        )
        pts_right[0] = self.front_right.add_vector(length_vec).add_vector(width_vec)

        length_vec = Vector(self.front_left, self.front_right).orthogonal_vector(
            self.length / 15, TurnDir.RIGHT
        )
        width_vec = Vector(self.rear_left, self.front_left).orthogonal_vector(
            self.width / 8, TurnDir.RIGHT
        )
        pts_left[1] = pts_left[0].add_vector(width_vec).add_vector(length_vec)

        width_vec = Vector(self.rear_left, self.front_left).orthogonal_vector(
            self.width / 8, TurnDir.LEFT
        )
        pts_right[1] = pts_right[0].add_vector(width_vec).add_vector(length_vec)

        length_vec = Vector(self.front_left, self.front_right).orthogonal_vector(
            self.length * 4 / 15, TurnDir.RIGHT
        )
        pts_left[2] = pts_left[1].add_vector(length_vec)
        pts_right[2] = pts_right[1].add_vector(length_vec)

        length_vec = Vector(self.front_left, self.front_right).orthogonal_vector(
            self.length * 6 / 15, TurnDir.RIGHT
        )
        pts_left[3] = pts_left[0].add_vector(length_vec)
        pts_right[3] = pts_right[0].add_vector(length_vec)

        pygame.draw.polygon(self.screen, "black", tuples_list(pts_left))
        pygame.draw.polygon(self.screen, "black", tuples_list(pts_right))

    def draw_back_window(self):
        pts = [Point(0, 0) for i in range(4)]

        length_vec = Vector(self.front_left, self.front_right).orthogonal_vector(
            self.length // 7, TurnDir.LEFT
        )
        width_vec = Vector(self.rear_left, self.front_left).orthogonal_vector(
            self.width / 4, TurnDir.RIGHT
        )
        pts[0] = self.rear_left.add_vector(length_vec).add_vector(width_vec)

        width_vec = Vector(self.rear_left, self.front_left).orthogonal_vector(
            self.width / 2, TurnDir.RIGHT
        )
        pts[1] = pts[0].add_vector(width_vec)

        length_vec = Vector(self.front_left, self.front_right).orthogonal_vector(
            self.length // 15, TurnDir.LEFT
        )
        width_vec = Vector(self.rear_left, self.front_left).orthogonal_vector(
            self.width / 8, TurnDir.RIGHT
        )
        pts[3] = pts[0].add_vector(width_vec).add_vector(length_vec)

        width_vec = Vector(self.rear_left, self.front_left).orthogonal_vector(
            self.width // 4, TurnDir.RIGHT
        )
        pts[2] = pts[3].add_vector(width_vec)

        pygame.draw.polygon(self.screen, "black", tuples_list(pts))

    def draw_wheels(self):
        wheel_left_pts = [Point(0, 0) for i in range(4)]
        wheel_right_pts = [Point(0, 0) for i in range(4)]

        wheel_left_pts[0].copy_coordinates_from(self.front_left)
        wheel_right_pts[0].copy_coordinates_from(self.front_right)
        length_vec = Vector(self.front_left, self.front_right).orthogonal_vector(
            self.length // 4, TurnDir.RIGHT
        )
        wheel_left_pts[1] = self.front_left.add_vector(length_vec)
        wheel_right_pts[1] = self.front_right.add_vector(length_vec)

        width_vec = Vector(self.rear_left, self.front_left).orthogonal_vector(
            self.width // 8, TurnDir.RIGHT
        )
        wheel_left_pts[3] = wheel_left_pts[0].add_vector(width_vec)
        wheel_left_pts[2] = wheel_left_pts[1].add_vector(width_vec)

        width_vec = Vector(self.rear_left, self.front_left).orthogonal_vector(
            self.width // 8, TurnDir.LEFT
        )
        wheel_right_pts[3] = wheel_right_pts[0].add_vector(width_vec)
        wheel_right_pts[2] = wheel_right_pts[1].add_vector(width_vec)

        length_vec = Vector(self.front_left, self.front_right).orthogonal_vector(
            self.length // 8, TurnDir.RIGHT
        )
        width_vec = Vector(self.rear_left, self.front_left).orthogonal_vector(
            self.width / 16, TurnDir.RIGHT
        )
        rotate_point_left = self.front_left.add_vector(length_vec).add_vector(width_vec)

        width_vec = Vector(self.rear_left, self.front_left).orthogonal_vector(
            self.width // 16, TurnDir.LEFT
        )
        rotate_point_right = self.front_right.add_vector(length_vec).add_vector(
            width_vec
        )

        for p1, p2 in zip(wheel_left_pts, wheel_right_pts):
            p1.rotate_over_point(
                rotate_point_left, self.wheels_angle, self.cur_turn_side
            )
            p2.rotate_over_point(
                rotate_point_right, self.wheels_angle, self.cur_turn_side
            )

        pygame.draw.polygon(self.screen, "#262626", tuples_list(wheel_left_pts))
        pygame.draw.polygon(self.screen, "#262626", tuples_list(wheel_right_pts))

    def draw_inside(self):
        pts = [Point(0, 0) for i in range(4)]
        line_width = self.width // 20

        length_vec = Vector(self.front_left, self.front_right).orthogonal_vector(
            line_width, TurnDir.LEFT
        )
        width_vec = Vector(self.rear_left, self.front_left).orthogonal_vector(
            line_width, TurnDir.RIGHT
        )
        pts[0] = self.rear_left.add_vector(length_vec).add_vector(width_vec)

        length_vec = Vector(self.front_left, self.front_right).orthogonal_vector(
            self.length * 14 / 15 - line_width, TurnDir.LEFT
        )
        width_vec = Vector(self.rear_left, self.front_left).orthogonal_vector(
            self.width * 0.9, TurnDir.RIGHT
        )

        pts[1] = pts[0].add_vector(length_vec)
        pts[2] = pts[1].add_vector(width_vec)
        pts[3] = pts[0].add_vector(width_vec)

        pygame.draw.polygon(self.screen, self.color, tuples_list(pts))

    def draw(self, body: Rectangle, screen: Surface) -> None:
        """
        Draw the car on the screen

        :param body: Rectangle representing position of the car body
        :param screen: pygame screen to draw the car on
        """
        pygame.draw.polygon(screen, "black", tuples_list(body.corners_list))
