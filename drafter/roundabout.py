import pygame
from road_segments.roundabout.schemas import RoundaboutColors, RoundaboutParts
from schemas import CardinalDirection


class RoundaboutDrafter:
    """
    Class responsible for drawing the roundabout.
    """

    def __init__(
        self,
        roundabout_parts: RoundaboutParts,
        roundabout_colors: RoundaboutColors,
    ):
        self.roundabout_parts = roundabout_parts
        self.roundabout_colors = roundabout_colors
        self.road_width = (
            self.roundabout_parts["incoming_lines"][CardinalDirection.LEFT].width * 2
        )

    def draw(self, screen: pygame.Surface) -> None:
        pass
