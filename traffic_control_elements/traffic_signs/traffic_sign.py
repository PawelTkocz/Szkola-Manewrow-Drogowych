from enum import Enum
import math

import pygame
from animations.constants import IMAGES_DIR_PATH
from geometry.direction import Direction
from geometry.vector import Point
from road_elements_drafter import RoadElementsDrafter
from traffic_control_elements.traffic_control_element import TrafficControlElement


class TrafficSignName(Enum):
    A5 = "A5"
    D1 = "D1"
    A7 = "A7"
    B20 = "B20"
    T6a_LEFT = "T6a_LEFT"
    T6a_RIGHT = "T6a_RIGHT"
    T6c_LEFT = "T6c_LEFT"
    T6c_RIGHT = "T6c_RIGHT"


SIGN_WIDTH = 50


class TrafficSign(TrafficControlElement):
    def __init__(
        self,
        name: TrafficSignName,
        image_file_name: str,
    ) -> None:
        self.image = self._get_image(image_file_name)
        super().__init__(SIGN_WIDTH, self.image.get_height())
        self.rotated_image = self.image
        self.name = name

    def _get_image(self, image_file_name: str) -> pygame.Surface:
        image = pygame.image.load(
            f"{IMAGES_DIR_PATH}/{image_file_name}"
        ).convert_alpha()
        sign_height = image.get_height() * SIGN_WIDTH / image.get_width()
        return pygame.transform.scale(image, (SIGN_WIDTH, sign_height))

    def update_position(self, front_middle: Point, direction: Direction) -> None:
        super().update_position(front_middle, direction)
        self.rotated_image = pygame.transform.rotate(
            self.image, math.degrees(self.rotation_angle)
        )

    def draw_on_road(self, road_elements_drafter: RoadElementsDrafter) -> None:
        road_elements_drafter.blit_surface(self.rotated_image, self.center)
