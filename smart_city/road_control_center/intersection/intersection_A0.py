import pygame
from animations.constants import IMAGES_DIR_PATH
from road_segments.intersection.intersection import Intersection
from schemas import CardinalDirection
from smart_city.road_control_center.constants import SIGN_SIZE
from smart_city.road_control_center.intersection.intersection_control_center import (
    IntersectionControlCenter,
)
from smart_city.road_control_center.intersection.priority_to_the_right_rule import (
    PriorityToTheRightRule,
)

INTERSECTION = Intersection()
INTERSECTION_RULES = PriorityToTheRightRule()


class IntersectionI0ControlCenter(IntersectionControlCenter):
    def __init__(self) -> None:
        self.image = pygame.image.load(f"{IMAGES_DIR_PATH}/sign_A5.png")
        original_width, original_height = self.image.get_size()
        scale_ratio = SIGN_SIZE / original_width
        new_height = int(original_height * scale_ratio)
        self.image = pygame.transform.scale(self.image, (SIGN_SIZE, new_height))
        self.control_elements: dict[CardinalDirection, list[pygame.Surface]] = {
            CardinalDirection.DOWN: [self.image],
            CardinalDirection.LEFT: [
                pygame.transform.rotate(self.image, 270),
                pygame.transform.rotate(self.image, 270),
            ],
            CardinalDirection.RIGHT: [pygame.transform.rotate(self.image, 90)],
            CardinalDirection.UP: [pygame.transform.rotate(self.image, 180)],
        }
        x = {
            CardinalDirection.DOWN: [self.image],
            CardinalDirection.LEFT: [
                self.image,
                self.image,
            ],
            CardinalDirection.RIGHT: [self.image],
            CardinalDirection.UP: [self.image],
        }

        super().__init__(INTERSECTION, INTERSECTION_RULES, x, "Intersection_I0")
