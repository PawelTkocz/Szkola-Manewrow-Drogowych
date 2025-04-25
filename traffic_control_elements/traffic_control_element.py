import pygame
from animations.constants import IMAGES_DIR_PATH
from drafter.utils import blit_surface
from geometry.direction import Direction
from geometry.shapes.rectangle import DynamicRectangle
from geometry.vector import Point


class TrafficControlElement(DynamicRectangle):
    def __init__(
        self, state_images_file_names: list[str], width: float, start_state: int = 0
    ) -> None:
        if not state_images_file_names:
            raise ValueError("Image for at least one state must be provided.")
        self.current_state = start_state
        self.original_state_images = [
            self._get_image(image_file_name, width)
            for image_file_name in state_images_file_names
        ]
        self.rotated_state_images = self.original_state_images
        super().__init__(
            Point(0, 0),
            width,
            self.original_state_images[0].get_height(),
            Direction(Point(0, 1)),
        )
        self._image_top_left = self.front_left

    def _get_image(self, image_file_name: str, width: float) -> pygame.Surface:
        image = pygame.image.load(f"{IMAGES_DIR_PATH}/{image_file_name}")
        image_width, image_height = image.get_size()
        height = int(image_height * width / image_width)
        return pygame.transform.scale(image, (width, height))

    def set_state(self, state_index: int) -> None:
        self.current_state = state_index

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
        self.rotated_images = [
            pygame.transform.rotate(original_image, rotation_angle)
            for original_image in self.original_state_images[:]
        ]

    def draw(
        self,
        screen: pygame.Surface,
        *,
        scale_factor: float = 1,
        screen_y_offset: int = 0,
    ) -> None:
        blit_surface(
            screen,
            self.rotated_images[self.current_state],
            self._image_top_left,
            scale_factor=scale_factor,
            screen_y_offset=screen_y_offset,
        )
