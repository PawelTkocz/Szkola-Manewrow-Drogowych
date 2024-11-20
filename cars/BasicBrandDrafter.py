from typing import List
from pygame import Surface
import pygame
from Geometry import Directions, Point, Rectangle, Vector
from drawing.utils import (
    PartRelativePosition,
    get_corners_center,
    get_symmetrical_shape,
    tuples_list,
)

# remember to change:
# each brand should specify the position of each car part
# the car should also have same property with info about each part color
# then, the clas CarDrafter could be initialized with Brand class and Coloristics info
# and then draw the car based on this info


class CarPartDrafter:
    """
    Class responsible for providing basic functions for drawing car parts
    """

    def __init__(
        self,
        color: str,
        corners_positions: List[PartRelativePosition],
    ):
        self.color = color
        self.corners_positions = corners_positions

    def get_current_corners_positions(self, body: Rectangle) -> List[Point]:
        corners = []
        length_vector = body.direction.get_negative_of_a_vector()
        width_vector = body.direction.get_orthogonal_vector(Directions.RIGHT)
        for corner_position in self.corners_positions:
            length_position_vector = length_vector.copy().scale_to_len(
                corner_position.length_pos * body.length
            )
            width_position_vector = width_vector.copy().scale_to_len(
                corner_position.width_pos * body.width
            )
            corners.append(
                body.front_left.copy()
                .add_vector(length_position_vector)
                .add_vector(width_position_vector)
            )
        return corners

    def draw(self, screen: Surface, body: Rectangle):
        corners = self.get_current_corners_positions(body)
        pygame.draw.polygon(screen, self.color, tuples_list(corners))


class WheelDrafter(CarPartDrafter):
    def __init__(
        self,
        corners_positions: List[PartRelativePosition],
        color,
    ):
        super().__init__(color, corners_positions)

    def draw(self, screen: Surface, body: Rectangle, angle: float):
        corners = super().get_current_corners_positions(body)
        rotation_point = get_corners_center(corners)
        rotated_corners = [
            corner.rotate_over_point(rotation_point, angle) for corner in corners
        ]
        pygame.draw.polygon(screen, self.color, tuples_list(rotated_corners))


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

    def __init__(self, color: str = "#262626"):
        self.left_wheel = WheelDrafter(self.corners_positions_left, color)
        self.right_wheel = WheelDrafter(self.corners_positions_rigth, color)

    def draw(self, screen: Surface, body: Rectangle, angle: float):
        self.left_wheel.draw(screen, body, angle)
        self.right_wheel.draw(screen, body, angle)


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

    def __init__(self, color: str = "black"):
        self.left_mirror = CarPartDrafter(color, self.corners_positions_left)
        self.right_mirror = CarPartDrafter(color, self.corners_positions_rigth)

    def draw(self, screen: Surface, body: Rectangle):
        self.left_mirror.draw(screen, body)
        self.right_mirror.draw(screen, body)


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

    def __init__(self, color: str = "yellow"):
        self.left_light = CarPartDrafter(color, self.corners_positions_left)
        self.right_light = CarPartDrafter(color, self.corners_positions_rigth)

    def draw(self, screen: Surface, body: Rectangle):
        self.left_light.draw(screen, body)
        self.right_light.draw(screen, body)


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

    def __init__(self, color: str = "black"):
        super().__init__(color, self.corners_positions)


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

    def __init__(self, color: str = "black"):
        super().__init__(color, self.corners_positions)


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

    def __init__(self, color: str = "black"):
        self.left_side_window = CarPartDrafter(color, self.corners_positions_left)
        self.right_side_window = CarPartDrafter(color, self.corners_positions_rigth)

    def draw(self, screen: Surface, body: Rectangle):
        self.left_side_window.draw(screen, body)
        self.right_side_window.draw(screen, body)


class BodyPanels(CarPartDrafter):
    """
    Class responsible for drawing body of the car
    """

    corners_positions = [
        PartRelativePosition(1 / 15, 0.05),
        PartRelativePosition(1 / 15, 0.95),
        PartRelativePosition(29 / 30, 0.95),
        PartRelativePosition(29 / 30, 0.05),
    ]

    def __init__(
        self,
        color: str = "red",
        bumper_color: str = "black",
    ):
        super().__init__(color, self.corners_positions)
        self.bumper_color = bumper_color

    def draw(self, screen: Surface, body: Rectangle):
        pygame.draw.polygon(screen, self.bumper_color, tuples_list(body.corners_list))
        super().draw(screen, body)


class BasicBrandDrafter:
    """
    Class responsible for drawing basic brand car on the screen
    """

    def __init__(self, color: str):
        """
        Initialize the drafter of basic brand cars

        :param width: width of the car
        :param length: length of the car
        :param color: color of the car
        """
        self.wheels = Wheels()
        self.body_panels = BodyPanels(color)
        self.lights = FrontLights()
        self.side_mirrors = SideMirrors()
        self.front_window = FrontWindow()
        self.side_windows = SideWindows()
        self.back_window = BackWindow()

    def draw(self, body: Rectangle, wheels_angle: float, screen: Surface) -> None:
        """
        Draw the car on the screen

        :param body: Rectangle representing position of the car body
        :param screen: pygame screen to draw the car on
        """
        self.wheels.draw(screen, body, wheels_angle)
        self.body_panels.draw(screen, body)
        self.lights.draw(screen, body)
        self.side_mirrors.draw(screen, body)
        self.front_window.draw(screen, body)
        self.side_windows.draw(screen, body)
        self.back_window.draw(screen, body)
