import pygame
from geometry.shapes.rectangle import AxisAlignedRectangle, Rectangle
from road_segments.intersection.schemas import (
    IntersectionColoristics,
    IntersectionParts,
)


class IntersectionDrafter:
    """
    Class responsible for drawing the intersection.
    """

    def __init__(
        self,
        intersection_parts: IntersectionParts,
        turn_curve: int,
        lines: list[Rectangle],
        coloristics: IntersectionColoristics,
        pavements: list[AxisAlignedRectangle],
    ):
        self.intersection_parts = intersection_parts
        self.lines = lines
        self.coloristics = coloristics
        self.road_width = self.intersection_parts["intersection_area"].width
        self.turn_curve = turn_curve
        self.pavements = pavements

    def draw_pavements(
        self,
        screen: pygame.Surface,
        *,
        scale_factor: float = 1,
        screen_y_offset: int = 0,
    ) -> None:
        for pavement in self.pavements:
            pavement.draw(
                screen, scale_factor=scale_factor, screen_y_offset=screen_y_offset
            )

    def draw_lines(
        self,
        screen: pygame.Surface,
        *,
        scale_factor: float = 1,
        screen_y_offset: int = 0,
    ) -> None:
        for line in self.lines:
            line.draw(
                screen, scale_factor=scale_factor, screen_y_offset=screen_y_offset
            )

    def draw(
        self,
        screen: pygame.Surface,
        *,
        scale_factor: float = 1,
        screen_y_offset: int = 0,
    ) -> None:
        screen.fill(self.coloristics["street"])
        self.draw_pavements(
            screen, scale_factor=scale_factor, screen_y_offset=screen_y_offset
        )
        self.draw_lines(
            screen, scale_factor=scale_factor, screen_y_offset=screen_y_offset
        )
