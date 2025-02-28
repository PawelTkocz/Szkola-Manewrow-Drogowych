from abc import ABC, abstractmethod
from car.car import LiveCarData
from constants import SCREEN_HEIGHT, SCREEN_WIDTH
from drafter.intersection import IntersectionDrafter
from geometry import Direction, Directions, Point, Rectangle
from intersection.schemas import CarOnIntersection, IntersectionParts


# remember to change from line to lane
class Intersection(ABC):
    def __init__(self, line_width):
        self.line_width = line_width
        self.intersection_parts = self._calculate_intersection_parts(line_width)
        self.intersection_drafter = IntersectionDrafter(self.intersection_parts)
        self.cars: list[CarOnIntersection] = []

    def _calculate_intersection_parts(self, line_width: float) -> IntersectionParts:
        street_width = 2 * line_width
        vertical_lines_length = (SCREEN_HEIGHT - street_width) / 2
        horizontal_lines_length = (SCREEN_WIDTH - street_width) / 2
        screen_middle = Point(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        return {
            "intersection_area": Rectangle(
                Point(screen_middle.x, vertical_lines_length),
                street_width,
                street_width,
                Direction(Point(0, 1)),
            ),
            "incoming_lines": {
                Directions.UP: Rectangle(
                    Point(screen_middle.x - line_width / 2, vertical_lines_length),
                    line_width,
                    vertical_lines_length,
                    Direction(Point(0, -1)),
                ),
                Directions.RIGHT: Rectangle(
                    Point(
                        screen_middle.x + line_width, screen_middle.y - line_width / 2
                    ),
                    line_width,
                    horizontal_lines_length,
                    Direction(Point(-1, 0)),
                ),
                Directions.DOWN: Rectangle(
                    Point(
                        screen_middle.x + line_width / 2, screen_middle.y + line_width
                    ),
                    line_width,
                    vertical_lines_length,
                    Direction(Point(0, 1)),
                ),
                Directions.LEFT: Rectangle(
                    Point(
                        screen_middle.x - line_width, screen_middle.y + line_width / 2
                    ),
                    line_width,
                    horizontal_lines_length,
                    Direction(Point(1, 0)),
                ),
            },
            "outcoming_lines": {
                Directions.UP: Rectangle(
                    Point(screen_middle.x + line_width / 2, 0),
                    line_width,
                    vertical_lines_length,
                    Direction(Point(0, 1)),
                ),
                Directions.RIGHT: Rectangle(
                    Point(SCREEN_WIDTH, screen_middle.y + line_width / 2),
                    line_width,
                    horizontal_lines_length,
                    Direction(Point(1, 0)),
                ),
                Directions.DOWN: Rectangle(
                    Point(screen_middle.x - line_width / 2, SCREEN_HEIGHT),
                    line_width,
                    vertical_lines_length,
                    Direction(Point(0, -1)),
                ),
                Directions.LEFT: Rectangle(
                    Point(0, screen_middle.y - line_width / 2),
                    line_width,
                    horizontal_lines_length,
                    Direction(Point(-1, 0)),
                ),
            },
        }

    def draw(self, screen):
        self.intersection_drafter.draw(screen)

    def add_car(
        self, live_car_data: LiveCarData, starting_side: Directions, ending_side: Directions
    ):
        self.cars.append(
            {
                "live_car_data": live_car_data,
                "starting_side": starting_side,
                "ending_side": ending_side,
            }
        )

    def remove_car(self, car_on_intersection: CarOnIntersection):
        self.cars.remove(car_on_intersection)

    def get_cars(self) -> list[CarOnIntersection]:
        return self.cars

    @abstractmethod
    def has_priority(car1: CarOnIntersection, car2: CarOnIntersection) -> bool:
        pass
