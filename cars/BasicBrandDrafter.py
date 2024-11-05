from typing import List
from pygame import Surface
import pygame
from Geometry import Directions, Point, Rectangle, Vector
from drawing.utils import (
    get_symmetrical_shape,
    tuples_list,
)


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
    corners_positions_rigth = get_symmetrical_shape(corners_positions_left)

    def __init__(self, body: Rectangle, screen: Surface, color: str = "#262626"):
        self.left_wheel = WheelDrafter(body, screen, self.corners_positions_left, color)
        self.right_wheel = WheelDrafter(
            body, screen, self.corners_positions_rigth, color
        )

    def draw(self, body: Rectangle, angle: float):
        self.left_wheel.draw(body, angle)
        self.right_wheel.draw(body, angle)


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
    corners_positions_rigth = get_symmetrical_shape(corners_positions_left)

    def __init__(self, body: Rectangle, screen: Surface, color: str = "black"):
        self.left_mirror = CarPartDrafter(
            screen, color, self.corners_positions_left, body
        )
        self.right_mirror = CarPartDrafter(
            screen, color, self.corners_positions_rigth, body
        )

    def draw(self, body: Rectangle):
        self.left_mirror.draw(body)
        self.right_mirror.draw(body)


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
    corners_positions_rigth = get_symmetrical_shape(corners_positions_left)

    def __init__(self, body: Rectangle, screen: Surface, color: str = "yellow"):
        self.left_light = CarPartDrafter(
            screen, color, self.corners_positions_left, body
        )
        self.right_light = CarPartDrafter(
            screen, color, self.corners_positions_rigth, body
        )

    def draw(self, body: Rectangle):
        self.left_light.draw(body)
        self.right_light.draw(body)


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


class BackWindow(CarPartDrafter):
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


class SideWindows:
    """
    Class responsible for drawing side windows
    """

    corners_positions_left = [
        PartRelativePosition(0.4, 0.125),
        PartRelativePosition(7 / 15, 0.25),
        PartRelativePosition(11 / 15, 0.25),
        PartRelativePosition(0.8, 0.125),
    ]
    corners_positions_rigth = get_symmetrical_shape(corners_positions_left)

    def __init__(self, body: Rectangle, screen: Surface, color: str = "black"):
        self.left_side_window = CarPartDrafter(
            screen, color, self.corners_positions_left, body
        )
        self.right_side_window = CarPartDrafter(
            screen, color, self.corners_positions_rigth, body
        )

    def draw(self, body: Rectangle):
        self.left_side_window.draw(body)
        self.right_side_window.draw(body)


class BodyPanels(CarPartDrafter):
    """
    Class responsible for drawing body of the car
    """

    corners_positions = [
        PartRelativePosition(0.1, 0.05),
        PartRelativePosition(0.1, 0.95),
        PartRelativePosition(0.9, 0.95),
        PartRelativePosition(0.9, 0.05),
    ]

    def __init__(
        self,
        body: Rectangle,
        screen: Surface,
        color: str = "red",
        bumper_color: str = "black",
    ):
        super().__init__(screen, color, self.corners_positions, body)
        self.bumper_color = bumper_color

    def draw(self, body: Rectangle):
        pygame.draw.polygon(
            self.screen, self.bumper_color, tuples_list(body.corners_list)
        )
        super().draw(body)


class BasicBrandDrafter:
    """
    Class responsible for drawing basic brand car on the screen
    """

    def __init__(self, body: Rectangle, color: str, screen: Surface):
        """
        Initialize the drafter of basic brand cars

        :param width: width of the car
        :param length: length of the car
        :param color: color of the car
        """
        self.color = color
        self.wheels = Wheels(body, screen)
        self.body_panels = BodyPanels(body, screen)
        self.lights = FrontLights(body, screen)
        self.side_mirrors = SideMirrors(body, screen)
        self.front_window = FrontWindow(body, screen)
        self.side_windows = SideWindows(body, screen)
        self.back_window = BackWindow(body, screen)

    def draw(self, body: Rectangle, screen: Surface) -> None:
        """
        Draw the car on the screen

        :param body: Rectangle representing position of the car body
        :param screen: pygame screen to draw the car on
        """
        self.wheels.draw(body, 0)
        self.body_panels.draw(body)
        self.lights.draw(body)
        self.side_mirrors.draw(body)
        self.front_window.draw(body)
        self.side_windows.draw(body)
        self.back_window.draw(body)
