import math

from Geometry import Direction, Directions, Point, Rectangle
from animations.intersection.Intersection import Intersection
from animations.intersection.constants import ROAD_WIDTH, SCREEN_HEIGHT, SCREEN_WIDTH


import pygame

read_movement_from_file = True


class IntersectionGoStraight:
    def __init__(self):
        self.intersection = Intersection(read_movement_from_file, "go_straight")
        self.intersection.add_car(
            Directions.DOWN,
            Directions.RIGHT,
            700,
            None,
            [],
        )
        self.intersection.add_car(
            Directions.LEFT,
            Directions.RIGHT,
            700,
            Rectangle(
                Point(
                    SCREEN_WIDTH / 2,
                    SCREEN_HEIGHT - (SCREEN_HEIGHT - ROAD_WIDTH) / 2,
                ),
                ROAD_WIDTH,
                ROAD_WIDTH,
                Direction(Point(0, 1)),
            ),
            [0],
        )
        self.intersection.add_car(
            Directions.RIGHT,
            Directions.DOWN,
            700,
            Rectangle(
                Point(
                    SCREEN_WIDTH / 2,
                    SCREEN_HEIGHT - (SCREEN_HEIGHT - ROAD_WIDTH) / 2,
                ),
                ROAD_WIDTH,
                ROAD_WIDTH,
                Direction(Point(0, 1)),
            ),
            [1],
        )

    def next_frame(self):
        self.intersection.draw()
        self.intersection.move()

    def save_cars_movement(self):
        self.intersection.save_cars_movement()


pygame.init()
clock = pygame.time.Clock()
game = IntersectionGoStraight()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            if not read_movement_from_file:
                game.save_cars_movement()
            pygame.quit()
            exit()

    game.next_frame()
    pygame.display.update()
    clock.tick(30)
