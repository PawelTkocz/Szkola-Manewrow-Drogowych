from enum import Enum

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
        image = pygame.image.load(f"{IMAGES_DIR_PATH}/{image_file_name}")
        sign_height = image.get_height() * SIGN_WIDTH / image.get_width()
        scaled_image = pygame.transform.scale(image, (SIGN_WIDTH, sign_height))
        super().__init__(SIGN_WIDTH, sign_height)
        self.image = scaled_image
        self.rotated_image = self.image
        self.name = name

    def update_position(self, front_middle: Point, direction: Direction) -> None:
        super().update_position(front_middle, direction)
        self.rotated_image = pygame.transform.rotate(self.image, self.rotation_angle)

    def draw_on_road(self, road_elements_drafter: RoadElementsDrafter) -> None:
        road_elements_drafter.blit_surface(self.rotated_image, self._image_top_left)
