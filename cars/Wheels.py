from Geometry import Direction, Directions, Point


class Wheels:
    """Class representing the state of the wheels in car"""

    def __init__(self, max_angle: float, direction: Direction = Direction(Point(1, 0))):
        self.max_angle = max_angle
        self.min_angle = max_angle * -1
        self.direction = direction.copy()
        self.max_left_direction = Direction(Point(1, 0)).turn(max_angle)
        self.max_right_direction = Direction(Point(1, 0)).turn(self.min_angle)

    @property
    def current_direction(self) -> Directions:
        angle = self.direction.angle
        if angle == 0:
            return Directions.FRONT
        return Directions.LEFT if angle > 0 else Directions.RIGHT

    @property
    def angle(self) -> float:
        return self.direction.angle

    def turn_left(self, angle: float) -> bool:
        if self.direction.compare(self.max_left_direction):
            return False
        self.direction.turn(angle)
        if self.direction.angle > self.max_angle:
            self.direction = self.max_left_direction.copy()
        return True

    def turn_right(self, angle: float) -> bool:
        if self.direction.compare(self.max_right_direction):
            return False
        self.direction.turn(angle)
        if self.direction.angle < self.min_angle:
            self.direction = self.max_right_direction.copy()
        return True

    def turn(self, angle: float, turn_direction: Directions) -> bool:
        return (
            self.turn_left(angle)
            if turn_direction == Directions.LEFT
            else self.turn_right(-1 * angle)
        )
