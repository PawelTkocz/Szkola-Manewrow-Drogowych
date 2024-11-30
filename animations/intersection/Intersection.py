import math

from Geometry import Directions
from animations.intersection.StreetIntersection import StreetIntersection
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
        self.cars = []
        self.autonomous_drivings = []

        start_position, direction, track_points = (
            self.street_intersection.prepare_car_ride(
                Directions.DOWN, Directions.UP, 700
            )
        )
        # self.autonomous_driving = BasicAutonomousDriving(self.car, Manoeuvre(...))
        # self.autonomous_driving.move(other_cars)
        self.cars.append(Car(BasicBrand(), start_position, direction))
        self.autonomous_drivings.append(
            BasicAutonomousDriving(self.cars[-1], track_points)
        )
        start_position2, direction2, track_points2 = (
            self.street_intersection.prepare_car_ride(
                Directions.LEFT, Directions.RIGHT, 700
            )
        )
        self.cars.append(Car(BasicBrand(), start_position2, direction2))
        self.autonomous_drivings.append(
            BasicAutonomousDriving(self.cars[-1], track_points2)
        )

        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))

        self.counter = 0

    def draw(self):
        self.street_intersection.draw(self.screen)
        for car in self.cars:
            car.draw(self.screen)

    def next_frame(self):
        self.counter += 1
        for autonomous_driving in self.autonomous_drivings:
            autonomous_driving.move([])


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
