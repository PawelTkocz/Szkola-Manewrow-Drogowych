from typing import List
from pygame import Surface
import pygame
from Geometry import Directions, Point, Rectangle, Vector
from drawing.utils import get_rectangle_corners, tuples_list


class PartRelativePosition:
    def __init__(self, length_pos: float, width_pos: float):
        """ """
        self.length_pos = length_pos
        self.width_pos = width_pos


class CarPartDrafter:
    """
    Class responsible for providing basic functions for drawing car parts
    """

    def __init__(
        self,
        screen: Surface,
        color: str,
        corners_positions: List[PartRelativePosition],
        body: Rectangle,
    ):
        self.screen = screen
        self.color = color
        self.corners_positions = corners_positions
        self.length = body.length
        self.width = body.width

    def get_current_corners_positions(self, body: Rectangle):
        corners = []
        length_vector = body.direction.get_negative_of_a_vector()
        width_vector = body.direction.get_orthogonal_vector(Directions.RIGHT)
        for corner_position in self.corners_positions:
            length_position_vector = length_vector.copy().scale_to_len(
                corner_position.length_pos * self.length
            )
            width_position_vector = width_vector.copy().scale_to_len(
                corner_position.width_pos * self.width
            )
            corners.append(
                body.front_left.copy()
                .add_vector(length_position_vector)
                .add_vector(width_position_vector)
            )
        return corners

    def draw(self, body: Rectangle):
        corners = self.get_current_corners_positions(body)
        pygame.draw.polygon(self.screen, self.color, tuples_list(corners))


class WheelDrafter(CarPartDrafter):
    def __init__(
        self,
        body: Rectangle,
        screen: Surface,
        corners_positions: List[PartRelativePosition],
        color,
    ):
        super().__init__(screen, color, corners_positions, body)

    def draw(self, body: Rectangle, angle: float):
        corners = super().get_current_corners_positions(body)
        rotation_point = body.center
        rotated_corners = [
            corner.rotate_over_point(rotation_point, angle) for corner in corners
        ]
        pygame.draw.polygon(self.screen, self.color, tuples_list(rotated_corners))


class Wheels:
    """
    Class responsible for drawing front wheels
    """

    corners_positions_left = [
        PartRelativePosition(0, 0),
        PartRelativePosition(0, 1 / 8),
        PartRelativePosition(1 / 4, 1 / 8),
        PartRelativePosition(1 / 4, 0),
    ]
    corners_positions_rigth = [
        PartRelativePosition(0, 7 / 8),
        PartRelativePosition(0, 1),
        PartRelativePosition(1 / 4, 1),
        PartRelativePosition(1 / 4, 7 / 8),
    ]

    def __init__(self, body: Rectangle, screen: Surface, color: str = "#262626"):
        self.left_wheel = WheelDrafter(body, screen, self.corners_positions_left, color)
        self.right_wheel = WheelDrafter(
            body, screen, self.corners_positions_rigth, color
        )

    def draw(self, body: Rectangle):
        self.left_wheel.draw()
        self.right_wheel.draw()


class SideMirrors:
    """
    Class responsible for drawing side mirrors
    """

    corners_positions_left = [
        PartRelativePosition(0.25, 0),
        PartRelativePosition(0.3, 0),
        PartRelativePosition(0.3, -1 / 8),
        PartRelativePosition(0.25, -1 / 8),
    ]
    corners_positions_rigth = [
        PartRelativePosition(0.25, 1),
        PartRelativePosition(0.25, 1.125),
        PartRelativePosition(0.3, 1.125),
        PartRelativePosition(0.3, 1),
    ]

    def __init__(self, body: Rectangle, screen: Surface, color: str = "black"):
        self.left_mirror = CarPartDrafter(
            screen, color, self.corners_positions_left, body
        )
        self.right_mirror = CarPartDrafter(
            screen, color, self.corners_positions_rigth, body
        )

    def draw(self, body: Rectangle):
        self.left_mirror.draw()
        self.right_mirror.draw()


class FrontLights:
    """
    Class responsible for drawing front lights
    """

    corners_positions_left = [
        PartRelativePosition(0, 0),
        PartRelativePosition(0, 0.25),
        PartRelativePosition(1 / 15, 0.25),
        PartRelativePosition(1 / 15, 0),
    ]
    corners_positions_rigth = [
        PartRelativePosition(0, 0.75),
        PartRelativePosition(0, 1),
        PartRelativePosition(1 / 15, 1),
        PartRelativePosition(1 / 15, 0.75),
    ]

    def __init__(self, body: Rectangle, screen: Surface, color: str = "yellow"):
        self.left_light = CarPartDrafter(
            screen, color, self.corners_positions_left, body
        )
        self.right_light = CarPartDrafter(
            screen, color, self.corners_positions_rigth, body
        )

    def draw(self, body: Rectangle):
        self.left_light.draw()
        self.right_light.draw()


class FrontWindow(CarPartDrafter):
    """
    Class responsible for drawing front window
    """

    corners_positions = [
        PartRelativePosition(2 / 7, 1 / 8),
        PartRelativePosition(2 / 7, 7 / 8),
        PartRelativePosition(3 / 7, 3 / 4),
        PartRelativePosition(3 / 7, 1 / 4),
    ]

    def __init__(self, body: Rectangle, screen: Surface, color: str = "black"):
        super().__init__(screen, color, self.corners_positions, body)


class BackWindows(CarPartDrafter):
    """
    Class responsible for drawing back window
    """

    corners_positions = [
        PartRelativePosition(6 / 7, 1 / 4),
        PartRelativePosition(6 / 7, 3 / 4),
        PartRelativePosition(11 / 14, 5 / 8),
        PartRelativePosition(11 / 14, 3 / 8),
    ]

    def __init__(self, body: Rectangle, screen: Surface, color: str = "black"):
        super().__init__(screen, color, self.corners_positions, body)


# maybe implement function to generate list of corners position symetric to given in array


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
