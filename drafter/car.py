from pygame import Surface
import pygame
from Geometry import Directions, Point, Rectangle, tuples_list
from car.model import CarModel, CarPartPosition, CarPointPosition


class CarDrafter:
    """
    Class responsible for drawing car on the screen.
    """

    def __init__(self, model: CarModel, color: str):
        """
        Initialize the car drafter.

        :param model: car model
        :param color: color of the car
        """
        self.model = model
        self.color = color

    def _get_car_point_position(
        self, car_body: Rectangle, position: CarPointPosition
    ) -> Point:
        """
        Based on car point position, return current point position.
        """
        length_vector = car_body.direction
        width_vector = car_body.direction.get_orthogonal_vector(Directions.RIGHT)
        length_position_vector = length_vector.copy().scale_to_len(position["y"])
        width_position_vector = width_vector.copy().scale_to_len(position["x"])
        return (
            car_body.front_middle.copy()
            .add_vector(length_position_vector)
            .add_vector(width_position_vector)
        )

    def _get_car_part_corners(
        self, car_body: Rectangle, car_part_position: CarPartPosition
    ) -> list[Point]:
        """
        Based on car part position and current car position, return current car part corners.
        """
        return [
            self._get_car_point_position(car_body, corner_position)
            for corner_position in car_part_position
        ]

    def _draw_car_part(
        self,
        car_body: Rectangle,
        car_part_position: CarPartPosition,
        color: str,
        screen: Surface,
    ):
        corners = self._get_car_part_corners(car_body, car_part_position)
        pygame.draw.polygon(screen, color, tuples_list(corners))

    def _draw_body(
        self, car_body: Rectangle, screen: Surface, bumpers_color: str = "black"
    ):
        # Draw bumpers
        pygame.draw.polygon(screen, bumpers_color, tuples_list(car_body.corners_list))

        # Draw the car shell
        self._draw_car_part(
            car_body, self.model.appearance["shell"], self.color, screen
        )

    def _draw_lights(self, car_body: Rectangle, screen: Surface, color: str = "yellow"):
        for lights_side in ["left", "right"]:
            self._draw_car_part(
                car_body,
                self.model.appearance["front_lights"][lights_side],
                color,
                screen,
            )

    def _draw_side_mirrors(
        self, car_body: Rectangle, screen: Surface, color: str = "black"
    ):
        for mirror_side in ["left", "right"]:
            self._draw_car_part(
                car_body,
                self.model.appearance["side_mirrors"][mirror_side],
                color,
                screen,
            )

    def _draw_windows(self, car_body: Rectangle, screen: Surface, color: str = "black"):
        for window_position in ["front", "rear", "left", "right"]:
            self._draw_car_part(
                car_body,
                self.model.appearance["windows"][window_position],
                color,
                screen,
            )

    def _draw_wheels(
        self,
        car_body: Rectangle,
        screen: Surface,
        wheels_angle: float,
        color: str = "#262626",
    ):
        for wheel_side in ["left", "right"]:
            wheel_corners = self._get_car_part_corners(
                car_body, self.model.wheels_positions[wheel_side]["corners"]
            )
            wheel_middle = self._get_car_point_position(
                car_body, self.model.wheels_positions[wheel_side]["middle"]
            )
            rotated_wheel_corners = [
                corner.rotate_over_point(wheel_middle, wheels_angle)
                for corner in wheel_corners
            ]
            pygame.draw.polygon(screen, color, tuples_list(rotated_wheel_corners))

    def draw(self, car_body: Rectangle, wheels_angle: float, screen: Surface) -> None:
        """
        Draw the car on the screen.

        :param car_body: Rectangle representing position of the car body
        :wheels_angle: angle of the wheels turn
        :param screen: pygame screen to draw the car on
        """
        self._draw_wheels(car_body, screen, wheels_angle)
        self._draw_body(car_body, screen)
        self._draw_lights(car_body, screen)
        self._draw_side_mirrors(car_body, screen)
        self._draw_windows(car_body, screen)
