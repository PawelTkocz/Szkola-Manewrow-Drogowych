import pygame
from drafter.utils import draw_circle, draw_rectangle
from geometry import Point, Rectangle
from road_segments.constants import LINES_WIDTH
from road_segments.intersection.schemas import IntersectionColors, IntersectionParts
from schemas import CardinalDirection


class IntersectionDrafter:
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

    def draw_street_curved_turns(self, screen: pygame.Surface) -> None:
        color = self.intersection_colors["street_color"]
        intersection_area = self.intersection_parts["intersection_area"]
        draw_rectangle(
            screen,
            color,
            Rectangle(
                Point(
                    intersection_area.center.x,
                    intersection_area.front_middle.y + self.turn_curve,
                ),
                intersection_area.width + 2 * self.turn_curve,
                intersection_area.length + 2 * self.turn_curve,
                intersection_area.direction,
            ),
        )

        pavement_color = self.intersection_colors["pavement_color"]
        draw_circle(
            screen,
            pavement_color,
            Point(
                intersection_area.front_left.x - self.turn_curve,
                intersection_area.front_left.y + self.turn_curve,
            ),
            self.turn_curve - 1,
        )
        draw_circle(
            screen,
            pavement_color,
            Point(
                intersection_area.front_right.x + self.turn_curve,
                intersection_area.front_right.y + self.turn_curve,
            ),
            self.turn_curve - 1,
        )
        draw_circle(
            screen,
            pavement_color,
            Point(
                intersection_area.rear_right.x + self.turn_curve,
                intersection_area.rear_right.y - self.turn_curve,
            ),
            self.turn_curve - 1,
        )
        draw_circle(
            screen,
            pavement_color,
            Point(
                intersection_area.rear_left.x - self.turn_curve,
                intersection_area.rear_left.y - self.turn_curve,
            ),
            self.turn_curve - 1,
        )

    def draw_street(self, screen: pygame.Surface) -> None:
        color = self.intersection_colors["street_color"]
        outcoming_lanes = self.intersection_parts["outcoming_lines"]
        intersection_area = self.intersection_parts["intersection_area"]
        vertical_length = (
            intersection_area.length + 2 * outcoming_lanes[CardinalDirection.UP].length
        )
        horizontal_length = (
            intersection_area.width + 2 * outcoming_lanes[CardinalDirection.LEFT].length
        )
        draw_rectangle(
            screen,
            color,
            Rectangle(
                outcoming_lanes[CardinalDirection.UP].front_left,
                self.road_width,
                vertical_length,
                outcoming_lanes[CardinalDirection.UP].direction,
            ),
        )
        draw_rectangle(
            screen,
            color,
            Rectangle(
                outcoming_lanes[CardinalDirection.LEFT].front_left,
                self.road_width,
                horizontal_length,
                outcoming_lanes[CardinalDirection.LEFT].direction,
            ),
        )
        self.draw_street_curved_turns(screen)

    def draw_lines(self, screen: pygame.Surface) -> None:
        lines_color = self.intersection_colors["lines_color"]
        outcoming_lines = self.intersection_parts["outcoming_lines"]
        for side in [
            CardinalDirection.UP,
            CardinalDirection.RIGHT,
            CardinalDirection.DOWN,
            CardinalDirection.LEFT,
        ]:
            draw_rectangle(
                screen,
                lines_color,
                Rectangle(
                    outcoming_lines[side].front_left,
                    LINES_WIDTH,
                    outcoming_lines[side].length,
                    outcoming_lines[side].direction,
                ),
            )

    def draw(self, screen: pygame.Surface) -> None:
        screen.fill(self.intersection_colors["pavement_color"])
        self.draw_street(screen)
        self.draw_lines(screen)
