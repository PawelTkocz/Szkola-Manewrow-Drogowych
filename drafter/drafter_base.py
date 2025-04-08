import pygame
from constants import SCREEN_HEIGHT
from geometry import Point, Rectangle, Vector


class DrafterBase:
    def get_pygame_coordinates(self, point: Point) -> tuple[float, float]:
        return (point.x, SCREEN_HEIGHT - point.y)

    def apply_y_screen_offset(self, point: Point, screen_y_offset: int) -> Point:
        return point.add_vector(Vector(Point(0, screen_y_offset)))

    def draw_polygon(
        self,
        screen: pygame.Surface,
        color: str,
        corners: list[Point],
        *,
        scale: float = 1,
        screen_y_offset: int = 0,
    ) -> None:
        corners_vectors = [Vector(corner) for corner in corners]
        pygame_corners = [
            self.get_pygame_coordinates(
                self.apply_y_screen_offset(corner_vector.scale(scale), screen_y_offset)
            )
            for corner_vector in corners_vectors
        ]
        pygame.draw.polygon(screen, color, pygame_corners)

    def draw_rectangle(
        self,
        screen: pygame.Surface,
        color: str,
        rect: Rectangle,
        *,
        scale: float = 1,
        screen_y_offset: int = 0,
    ) -> None:
        self.draw_polygon(
            screen,
            color,
            rect.corners_list,
            scale=scale,
            screen_y_offset=screen_y_offset,
        )

    def draw_circle(
        self,
        screen: pygame.Surface,
        color: str,
        center: Point,
        radius: float,
        *,
        scale: float = 1,
        screen_y_offset: int = 0,
    ) -> None:
        pygame.draw.circle(
            screen,
            color,
            self.get_pygame_coordinates(
                self.apply_y_screen_offset(Vector(center).scale(scale), screen_y_offset)
            ),
            radius * scale,
        )
