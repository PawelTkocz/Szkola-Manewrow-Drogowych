import math

from Geometry import Direction, Directions, Point, Rectangle
from animations.intersection.IntersectionManoeuvre import IntersectionManoeuvre
from animations.intersection.Manoeuvre import Manoeuvre
from animations.intersection.StreetIntersection import StreetIntersection
from animations.intersection.constants import ROAD_WIDTH, SCREEN_HEIGHT, SCREEN_WIDTH
from autonomousDriving.BasicAutonomousDriving import (
    BasicAutonomousDriving,
)
from cars.BasicBrand import BasicBrand
from cars.Car import Car

import pygame


# if it will still be lagging i can do sth like computation of max velocities for each point on the line before the animation starts
class Intersection:
    screen_height = 800
    screen_width = 1400

    def __init__(self):
        self.street_intersection = StreetIntersection()

        start_position, direction, track_points = (
            self.street_intersection.prepare_car_ride(
                Directions.DOWN, Directions.UP, 700
            )
        )
        self.intersection_manoeuvre1 = Manoeuvre(
            [
                IntersectionManoeuvre(
                    track_points,
                    Rectangle(
                        Point(
                            SCREEN_WIDTH / 2,
                            SCREEN_HEIGHT - (SCREEN_HEIGHT - ROAD_WIDTH) / 2,
                        ),
                        ROAD_WIDTH,
                        ROAD_WIDTH,
                        Direction(Point(0, 1)),
                    ),
                )
            ]
        )
        self.car1 = Car(BasicBrand(), start_position, direction)
        self.autonomous_driving1 = BasicAutonomousDriving(
            self.car1, self.intersection_manoeuvre1
        )

        start_position2, direction2, track_points2 = (
            self.street_intersection.prepare_car_ride(
                Directions.LEFT, Directions.RIGHT, 700
            )
        )
        self.intersection_manoeuvre2 = Manoeuvre(
            [IntersectionManoeuvre(track_points2, None)]
        )
        self.car2 = Car(BasicBrand(), start_position2, direction2)
        self.autonomous_driving2 = BasicAutonomousDriving(
            self.car2, self.intersection_manoeuvre2
        )

        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.counter = 0

    def draw(self):
        self.street_intersection.draw(self.screen)
        self.car1.draw(self.screen)
        self.car2.draw(self.screen)

    def next_frame(self):
        self.counter += 1
        self.autonomous_driving1.move([])
        self.autonomous_driving2.move([])


pygame.init()
clock = pygame.time.Clock()
game = Intersection()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    game.draw()
    game.next_frame()
    pygame.display.update()
    clock.tick(30)
