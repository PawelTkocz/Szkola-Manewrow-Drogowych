from __future__ import annotations
import numpy as np
from pygame import Surface
import pygame
from geometry.direction import Direction
from geometry.shapes.polygon import Polygon
from geometry.vector import Point, Vector
from schemas import HorizontalDirection
from utils import blit_surface


class Rectangle(Polygon):
    def __init__(
        self,
        front_middle: Point,
        width: float,
        length: float,
        direction: Direction,
        color: str = "black",
    ):
        self._width = width
        self._length = length
        self._direction = direction.copy()
        self._front_middle = front_middle.copy()
        self._calculate_corners_positions()
        super().__init__(self.corners_list, color)

    @property
    def width(self) -> float:
        return self._width

    @property
    def length(self) -> float:
        return self._length

    @property
    def direction(self) -> Direction:
        return self._direction.copy()

    @property
    def front_middle(self) -> Point:
        return self._front_middle.copy()

    @property
    def rear_middle(self) -> Point:
        return self._rear_middle.copy()

    @property
    def front_left(self) -> Point:
        return self._front_left.copy()

    @property
    def front_right(self) -> Point:
        return self._front_right.copy()

    @property
    def rear_left(self) -> Point:
        return self._rear_left.copy()

    @property
    def rear_right(self) -> Point:
        return self._rear_right.copy()

    def _calculate_corners_positions(self) -> None:
        width_vec = self.direction.get_orthogonal_vector(
            HorizontalDirection.RIGHT, self.width
        )
        length_vec = width_vec.get_orthogonal_vector(
            HorizontalDirection.RIGHT, self.length
        )
        self._front_left = self.front_middle.add_vector(
            width_vec.copy().scale(0.5).get_negative_of_a_vector()
        )
        self._front_right = self.front_left.add_vector(width_vec)
        self._rear_left = self.front_left.add_vector(length_vec)
        self._rear_right = self.rear_left.add_vector(width_vec)
        self._rear_middle = self.front_middle.add_vector(length_vec)

    @property
    def corners_list(self) -> list[Point]:
        return [
            self.rear_left,
            self.rear_right,
            self.front_right,
            self.front_left,
        ]

    @property
    def center(self) -> Point:
        vector = Vector(self.rear_right, self.front_left).scale(0.5)
        return self.front_left.add_vector(vector)

    def is_point_inside(self, point: Point) -> bool:
        np_point = np.array([point.x, point.y])
        corners = np.array([corner.to_tuple() for corner in self.corners_list])
        vectors = [corners[(i + 1) % 4] - corners[i] for i in range(4)]
        point_vectors = [np_point - corners[i] for i in range(4)]
        cross_products = [
            np.cross(vector, point_vector)
            for vector, point_vector in zip(vectors, point_vectors)
        ]
        return all(cross_product >= 0 for cross_product in cross_products) or all(
            cross_product <= 0 for cross_product in cross_products
        )

    def collides(self, rec: Rectangle) -> bool:
        return any(self.is_point_inside(corner) for corner in rec.corners_list) or any(
            rec.is_point_inside(corner) for corner in self.corners_list
        )


class AxisAlignedRectangle(Rectangle):
    def __init__(
        self,
        front_middle: Point,
        width: float,
        length: float,
        color: str = "black",
        border_front_left_radius: int = -1,
        border_front_right_radius: int = -1,
        border_rear_left_radius: int = -1,
        border_rear_right_radius: int = -1,
        transparency: int = 255,
    ) -> None:
        super().__init__(front_middle, width, length, Direction(Point(0, 1)), color)
        self.border_front_left_radius = border_front_left_radius
        self.border_front_right_radius = border_front_right_radius
        self.border_rear_left_radius = border_rear_left_radius
        self.border_rear_right_radius = border_rear_right_radius
        self.transparency = max(0, min(transparency, 255))
        pygame_color = pygame.Color(color)
        pygame_color.a = transparency
        self.pygame_color = pygame_color

    def get_surface(self) -> Surface:
        surface = pygame.Surface((self.width, self.length), pygame.SRCALPHA)
        pygame.draw.rect(
            surface,
            self.pygame_color,
            pygame.Rect(
                0,
                0,
                self.width,
                self.length,
            ),
            border_top_right_radius=self.border_front_right_radius,
            border_top_left_radius=self.border_front_left_radius,
            border_bottom_left_radius=self.border_rear_left_radius,
            border_bottom_right_radius=self.border_rear_right_radius,
        )
        return surface

    def draw(self, screen: Surface) -> None:
        surface = self.get_surface()
        blit_surface(screen, surface, self.front_left)


class DynamicRectangle(Rectangle):
    def update_position(self, front_middle: Point, direction: Direction) -> None:
        self._front_middle = front_middle
        self._direction = direction
        self._calculate_corners_positions()
        self.corners = self.corners_list
