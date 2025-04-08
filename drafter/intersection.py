import pygame
from drafter.drafter_base import DrafterBase
from geometry import Point, Rectangle
from road_segments.constants import LINES_WIDTH
from road_segments.intersection.schemas import IntersectionColors, IntersectionParts
from schemas import CardinalDirection


class IntersectionDrafter(DrafterBase):
    """
    Class responsible for drawing the intersection.
    """

    def __init__(
        self,
        intersection_parts: IntersectionParts,
        intersection_colors: IntersectionColors,
    ):
        self.intersection_parts = intersection_parts
        self.intersection_colors = intersection_colors
        self.road_width = self.intersection_parts["intersection_area"].width
        self.turn_curve = 90

    def draw_street_curved_turns(
        self, screen: pygame.Surface, *, scale: float = 1, screen_y_offset: int = 0
    ) -> None:
        turn_curve = self.turn_curve  # this should be in intersection specification
        color = self.intersection_colors["street_color"]
        intersection_area = self.intersection_parts["intersection_area"]
        self.draw_rectangle(
            screen,
            color,
            Rectangle(
                Point(
                    intersection_area.center.x,
                    intersection_area.front_middle.y + turn_curve,
                ),
                intersection_area.width + 2 * turn_curve,
                intersection_area.length + 2 * turn_curve,
                intersection_area.direction,
            ),
            scale=scale,
            screen_y_offset=screen_y_offset,
        )

        pavement_color = self.intersection_colors["pavement_color"]
        self.draw_circle(
            screen,
            pavement_color,
            Point(
                intersection_area.front_left.x - turn_curve,
                intersection_area.front_left.y + turn_curve,
            ),
            turn_curve - 1,
            scale=scale,
            screen_y_offset=screen_y_offset,
        )
        self.draw_circle(
            screen,
            pavement_color,
            Point(
                intersection_area.front_right.x + turn_curve,
                intersection_area.front_right.y + turn_curve,
            ),
            turn_curve - 1,
            scale=scale,
            screen_y_offset=screen_y_offset,
        )
        self.draw_circle(
            screen,
            pavement_color,
            Point(
                intersection_area.rear_right.x + turn_curve,
                intersection_area.rear_right.y - turn_curve,
            ),
            turn_curve - 1,
            scale=scale,
            screen_y_offset=screen_y_offset,
        )
        self.draw_circle(
            screen,
            pavement_color,
            Point(
                intersection_area.rear_left.x - turn_curve,
                intersection_area.rear_left.y - turn_curve,
            ),
            turn_curve - 1,
            scale=scale,
            screen_y_offset=screen_y_offset,
        )

    def draw_street(
        self, screen: pygame.Surface, *, scale: float = 1, screen_y_offset: int = 0
    ) -> None:
        color = self.intersection_colors["street_color"]
        outcoming_lanes = self.intersection_parts["outcoming_lines"]
        intersection_area = self.intersection_parts["intersection_area"]
        intersection_side = (
            intersection_area.length + 2 * outcoming_lanes[CardinalDirection.UP].length
        )
        self.draw_rectangle(
            screen,
            color,
            Rectangle(
                outcoming_lanes[CardinalDirection.UP].front_left,
                self.road_width,
                intersection_side,
                outcoming_lanes[CardinalDirection.UP].direction,
            ),
            scale=scale,
            screen_y_offset=screen_y_offset,
        )
        self.draw_rectangle(
            screen,
            color,
            Rectangle(
                outcoming_lanes[CardinalDirection.LEFT].front_left,
                self.road_width,
                intersection_side,
                outcoming_lanes[CardinalDirection.LEFT].direction,
            ),
            scale=scale,
            screen_y_offset=screen_y_offset,
        )
        self.draw_street_curved_turns(
            screen, scale=scale, screen_y_offset=screen_y_offset
        )

    def draw_lines(
        self, screen: pygame.Surface, *, scale: float = 1, screen_y_offset: int = 0
    ) -> None:
        lines_color = self.intersection_colors["lines_color"]
        outcoming_lanes = self.intersection_parts["outcoming_lines"]
        for side in CardinalDirection:
            self.draw_rectangle(
                screen,
                lines_color,
                Rectangle(
                    outcoming_lanes[side].front_left,
                    LINES_WIDTH,
                    outcoming_lanes[side].length,
                    outcoming_lanes[side].direction,
                ),
                scale=scale,
                screen_y_offset=screen_y_offset,
            )

    def draw(
        self, screen: pygame.Surface, *, scale: float = 1, screen_y_offset: int = 0
    ) -> None:
        screen.fill(self.intersection_colors["pavement_color"])
        self.draw_street(screen, scale=scale, screen_y_offset=screen_y_offset)
        self.draw_lines(screen, scale=scale, screen_y_offset=screen_y_offset)
