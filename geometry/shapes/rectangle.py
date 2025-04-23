import numpy as np
from pygame import Surface
import pygame
from drafter.utils import blit_surface
from geometry.direction import Direction
from geometry.shapes.polygon import Polygon
from geometry.vector import Point, Vector
from schemas import HorizontalDirection


class Rectangle(Polygon):
    def __init__(
        self,
        front_middle: Point,
        width: float,
        length: float,
        direction: Direction,
        color: str = "black",
    ):
        """
        Initialize directed rectangle

        :param front_middle: position of front middle point of the rectangle
        :param width: width of the rectangle (of front and rear sides)
        :param length: length of the rectangle (of left and right sides)
        :param direction: direction the rectangle is heading
        :return: directed rectangle with specified width, length and position
        """
        self._width = width
        self._length = length
        self._calculate_corners_positions(front_middle, direction)
        super().__init__(self.corners_list, color)

    @property
    def width(self) -> float:
        return self._width

    @property
    def length(self) -> float:
        return self._length

    @property
    def direction(self) -> Direction:
        """
        Get the current direction of the rectangle.
        """
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

    def _calculate_corners_positions(
        self, front_middle: Point, direction: Direction
    ) -> None:
        self._direction = direction.copy()
        self._front_middle = front_middle.copy()
        width_vec = direction.get_orthogonal_vector(
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
        """
        Get the list of corners coordinates.
        """
        return [
            self.rear_left,
            self.rear_right,
            self.front_right,
            self.front_left,
        ]

    @property
    def center(self) -> Point:
        """
        Get the center of rectangle.
        """
        vector = Vector(self.rear_right, self.front_left).scale(0.5)
        return self.front_left.add_vector(vector)

    def is_point_inside(self, p: Point) -> bool:
        point = np.array([p.x, p.y])
        rect = np.array([x.to_tuple() for x in self.corners_list])
        vectors = [rect[(i + 1) % 4] - rect[i] for i in range(4)]
        point_vectors = [point - rect[i] for i in range(4)]
        cross_products = [np.cross(v, pv) for v, pv in zip(vectors, point_vectors)]
        return all(cp >= 0 for cp in cross_products) or all(
            cp <= 0 for cp in cross_products
        )

    def collides(self, rec: "Rectangle") -> bool:
        return any(self.is_point_inside(p) for p in rec.corners_list) or any(
            rec.is_point_inside(p) for p in self.corners_list
        )

    def copy(self) -> "Rectangle":
        """
        Get copy of a rectangle
        """
        return Rectangle(
            self.front_middle, self.width, self.length, self.direction, self.color
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

    def draw(
        self,
        screen: Surface,
        *,
        scale_factor: float = 1,
        screen_y_offset: int = 0,
    ) -> None:
        scaled_width = self.width * scale_factor
        scaled_height = self.length * scale_factor
        surface = pygame.Surface((scaled_width, scaled_height), pygame.SRCALPHA)
        pygame.draw.rect(
            surface,
            self.pygame_color,
            pygame.Rect(
                0,
                0,
                scaled_width,
                scaled_height,
            ),
            border_top_right_radius=self.border_front_right_radius,
            border_top_left_radius=self.border_front_left_radius,
            border_bottom_left_radius=self.border_rear_left_radius,
            border_bottom_right_radius=self.border_rear_right_radius,
        )
        blit_surface(
            screen,
            surface,
            self.front_left,
            scale_factor=scale_factor,
            screen_y_offset=screen_y_offset,
        )


class DynamicRectangle(Rectangle):
    """
    Class representing 'directed' rectangle in Cartesian coordinate system

    'Directed' rectangle has its front, left and right side, and rear
    """

    def update_position(self, front_middle: Point, direction: Direction) -> None:
        self._calculate_corners_positions(front_middle, direction)
        self._corners = self.corners_list

    def enlarge_rectangle(self, v: float) -> "Rectangle":
        # move somewhere different
        return Rectangle(
            self.center.add_vector(self.direction.scale_to_len(self.length / 2 * v)),
            self.width * v,
            self.length * v,
            self.direction,
        )
