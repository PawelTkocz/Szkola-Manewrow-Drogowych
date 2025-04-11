import pygame
from geometry import Point, Rectangle, Vector
from utils import get_pygame_point


class DrafterBase:
    def point_to_tuple(self, point: Point) -> tuple[float, float]:
        return [point.x, point.y]

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
            self.point_to_tuple(
                get_pygame_point(
                    self.apply_y_screen_offset(
                        corner_vector.scale(scale), screen_y_offset
                    )
                )
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

    def draw_basic_rectangle(
        self,
        screen: pygame.Surface,
        color: str,
        front_left: Point,
        width: int,
        height: int,
        *,
        scale: float = 1,
        screen_y_offset: int = 0,
        border_front_left_radius: int = -1,
        border_front_right_radius: int = -1,
        border_rear_left_radius: int = -1,
        border_rear_right_radius: int = -1,
        transparency: int = 255,
    ) -> None:
        transparency = max(0, min(transparency, 255))
        pygame_color = pygame.Color(color)
        pygame_color.a = transparency

        scaled_width = width * scale
        scaled_height = height * scale
        surface = pygame.Surface((scaled_width, scaled_height), pygame.SRCALPHA)
        pygame.draw.rect(
            surface,
            pygame_color,
            pygame.Rect(
                0,
                0,
                scaled_width,
                scaled_height,
            ),
            border_top_right_radius=border_front_right_radius,
            border_top_left_radius=border_front_left_radius,
            border_bottom_left_radius=border_rear_left_radius,
            border_bottom_right_radius=border_rear_right_radius,
        )
        self.blit_surface(
            screen, surface, front_left, scale=scale, screen_y_offset=screen_y_offset
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
            self.point_to_tuple(
                get_pygame_point(
                    self.apply_y_screen_offset(
                        Vector(center).scale(scale), screen_y_offset
                    )
                )
            ),
            radius * scale,
        )

    def blit_surface(
        self,
        screen: pygame.Surface,
        surface: pygame.Surface,
        top_left: Point,
        *,
        scale: float = 1,
        screen_y_offset: int = 0,
    ) -> None:
        transformed_top_left = get_pygame_point(
            self.apply_y_screen_offset(Vector(top_left).scale(scale), screen_y_offset)
        )
        screen.blit(surface, self.point_to_tuple(transformed_top_left))
