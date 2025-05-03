from pygame import Surface
import pygame

from geometry.shapes.polygon import Polygon
from geometry.shapes.rectangle import AxisAlignedRectangle
from geometry.vector import Point, Vector
from utils import get_pygame_screen_point


class RoadElementsDrafter:
    def __init__(
        self, road_segment_area: AxisAlignedRectangle, screen: Surface
    ) -> None:
        self.scale_factor = screen.get_width() / road_segment_area.width
        self.screen_y_offset = int(
            (screen.get_height() - road_segment_area.length * self.scale_factor) // 2
        )
        self.screen = screen

    def _apply_screen_y_offset(self, point: Point) -> Point:
        return point.add_vector(Vector(Point(0, self.screen_y_offset)))

    def _get_pygame_coordinates(self, point: Point) -> tuple[float, float]:
        return get_pygame_screen_point(
            self.screen,
            self._apply_screen_y_offset(Vector(point).scale(self.scale_factor)),
        ).to_tuple()

    def draw_polygon(self, polygon: Polygon) -> None:
        pygame_corners = [
            self._get_pygame_coordinates(corner) for corner in polygon._corners
        ]
        pygame.draw.polygon(self.screen, polygon.color, pygame_corners)

    def blit_surface(
        self,
        surface: pygame.Surface,
        top_left: Point,
    ) -> None:
        scaled_surface = pygame.transform.scale(
            surface,
            (
                int(surface.get_width() * self.scale_factor),
                int(surface.get_height() * self.scale_factor),
            ),
        )
        self.screen.blit(
            scaled_surface,
            self._get_pygame_coordinates(top_left),
        )

    def draw_axis_aligned_rectangle(self, rectangle: AxisAlignedRectangle) -> None:
        surface = rectangle.get_surface()
        self.blit_surface(surface, rectangle.front_left)
