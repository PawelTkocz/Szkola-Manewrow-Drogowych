from constants import SCREEN_HEIGHT, SCREEN_WIDTH
from geometry import Direction, Directions, Point, Rectangle
from state import State
from animations.intersection.intersection import Intersection
from animations.intersection.constants import ROAD_WIDTH


class IntersectionTurnLeft(State):
    def __init__(self, previous_state: State, *, read_movement_from_file=True):
        super().__init__(previous_state=previous_state)
        self.read_movement_from_file = read_movement_from_file
        self.intersection = Intersection(read_movement_from_file, "turn_left")
        self.intersection.add_car(Directions.RIGHT, Directions.UP, 700, None)
        self.intersection.add_car(
            Directions.DOWN,
            Directions.UP,
            1000,
            Rectangle(
                Point(
                    SCREEN_WIDTH / 2 + ROAD_WIDTH / 4,
                    SCREEN_HEIGHT - (SCREEN_HEIGHT - ROAD_WIDTH) / 2,
                ),
                ROAD_WIDTH / 2,
                ROAD_WIDTH,
                Direction(Point(0, 1)),
            ),
        )
        self.intersection.add_car(
            Directions.LEFT,
            Directions.UP,
            600,
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

    def save_cars_movement(self):
        self.intersection.save_cars_movement()

    def render_frame(self, screen):
        self.intersection.draw(screen)
        self.intersection.move()

    def handle_click(self, mouse_click_position) -> State:
        return self.previous_state

    def handle_quit(self):
        if not self.read_movement_from_file:
            self.save_cars_movement()
