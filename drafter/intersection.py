import pygame
from drafter.utils import draw_axis_aligned_rectangle, draw_rectangle
from geometry import Point, Rectangle
from road_segments.intersection.schemas import (
    IntersectionColoristics,
    IntersectionParts,
)
from schemas import CardinalDirection


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
    ):
        self.intersection_parts = intersection_parts
        self.lines = lines
        self.coloristics = coloristics
        self.road_width = self.intersection_parts["intersection_area"].width
        self.turn_curve = turn_curve

    def draw_pavements(
        self,
        screen: pygame.Surface,
        *,
        scale_factor: float = 1,
        screen_y_offset: int = 0,
    ) -> None:
        pavement_color = self.coloristics["pavement"]
        outcoming_lanes = self.intersection_parts["outcoming_lanes"]
        incoming_lanes = self.intersection_parts["incoming_lanes"]
        draw_axis_aligned_rectangle(
            screen,
            pavement_color,
            Point(0, outcoming_lanes[CardinalDirection.UP].front_left.y),
            outcoming_lanes[CardinalDirection.LEFT].length,
            outcoming_lanes[CardinalDirection.UP].length,
            scale_factor=scale_factor,
            screen_y_offset=screen_y_offset,
            border_rear_right_radius=self.turn_curve,
        )
        draw_axis_aligned_rectangle(
            screen,
            pavement_color,
            outcoming_lanes[CardinalDirection.UP].front_right,
            outcoming_lanes[CardinalDirection.RIGHT].length,
            outcoming_lanes[CardinalDirection.UP].length,
            scale_factor=scale_factor,
            screen_y_offset=screen_y_offset,
            border_rear_left_radius=self.turn_curve,
        )
        draw_axis_aligned_rectangle(
            screen,
            pavement_color,
            incoming_lanes[CardinalDirection.LEFT].rear_right,
            outcoming_lanes[CardinalDirection.LEFT].length,
            outcoming_lanes[CardinalDirection.DOWN].length,
            scale_factor=scale_factor,
            screen_y_offset=screen_y_offset,
            border_front_right_radius=self.turn_curve,
        )
        draw_axis_aligned_rectangle(
            screen,
            pavement_color,
            incoming_lanes[CardinalDirection.DOWN].front_right,
            outcoming_lanes[CardinalDirection.LEFT].length,
            outcoming_lanes[CardinalDirection.DOWN].length,
            scale_factor=scale_factor,
            screen_y_offset=screen_y_offset,
            border_front_left_radius=self.turn_curve,
        )

    def draw_lines(
        self,
        screen: pygame.Surface,
        *,
        scale_factor: float = 1,
        screen_y_offset: int = 0,
    ) -> None:
        for line in self.lines:
            draw_rectangle(
                screen,
                self.coloristics["lines"],
                line,
                scale_factor=scale_factor,
                screen_y_offset=screen_y_offset,
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
