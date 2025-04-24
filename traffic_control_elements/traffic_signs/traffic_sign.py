from enum import Enum
import pygame

from animations.constants import IMAGES_DIR_PATH
from drafter.utils import blit_surface
from geometry.direction import Direction
from geometry.shapes.rectangle import DynamicRectangle
from geometry.vector import Point


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


class TrafficSign(DynamicRectangle):
    def __init__(
        self,
        name: TrafficSignName,
        image_file_name: str,
    ) -> None:
        self.original_image = self._get_image(image_file_name)
        self.directed_image = self.original_image
        super().__init__(
            Point(0, 0),
            SIGN_WIDTH,
            self.directed_image.get_height(),
            Direction(Point(0, 1)),
        )
        self.name = name
        self._image_top_left = self.front_left

    def _get_image(self, image_file_name: str) -> pygame.Surface:
        image = pygame.image.load(f"{IMAGES_DIR_PATH}/{image_file_name}.png")
        image_width, image_height = image.get_size()
        height = int(image_height * SIGN_WIDTH / image_width)
        return pygame.transform.scale(image, (SIGN_WIDTH, height))

    def update_position(self, front_middle: Point, direction: Direction) -> None:
        if not any(
            [
                direction.compare(Direction(Point(0, 1))),
                direction.compare(Direction(Point(0, -1))),
                direction.compare(Direction(Point(1, 0))),
                direction.compare(Direction(Point(-1, 0))),
            ]
        ):
            raise ValueError("Traffic control elements must by axis aligned.")
        super().update_position(front_middle, direction)
        if direction.compare(Direction(Point(0, 1))):
            self._image_top_left = self.front_left
            rotation_angle = 0
        elif direction.compare(Direction(Point(0, -1))):
            self._image_top_left = self.rear_right
            rotation_angle = 180
        elif direction.compare(Direction(Point(1, 0))):
            self._image_top_left = self.rear_left
            rotation_angle = 270
        else:
            self._image_top_left = self.front_right
            rotation_angle = 90
        self.directed_image = pygame.transform.rotate(
            self.original_image, rotation_angle
        )

    def draw(
        self,
        screen: pygame.Surface,
        *,
        scale_factor: float = 1,
        screen_y_offset: int = 0,
    ) -> None:
        blit_surface(
            screen,
            self.directed_image,
            self._image_top_left,
            scale_factor=scale_factor,
            screen_y_offset=screen_y_offset,
        )


# move scale factor and y offset to some global variables
