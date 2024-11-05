from pygame import Surface
from Geometry import Direction, Point, Rectangle, Vector
from cars.BasicBrand import BasicBrand
from cars.Brand import Brand


class Car:
    """
    Class representing a car in Cartesian coordinate system
    """

    def __init__(
        self,
        brand: Brand,
        front_left_position: Point,
        direction: Direction = Direction(Point(1, 0)),
        velocity: float = 0,
        reversing: bool = False,
    ):
        """
        Initialize car
        """
        self.brand = brand
        self.reversing = reversing
        self.velocity = velocity
        self.body = Rectangle(front_left_position, brand.width, brand.length, direction)

    @property
    def direction(self):
        return self.body.direction

    @property
    def front_left(self):
        return self.body.front_left

    @property
    def front_right(self):
        return self.body.front_right

    @property
    def rear_left(self):
        return self.body.rear_left

    @property
    def rear_right(self):
        return self.body.rear_right

    def draw(self, screen):
        self.brand.draw(self.body, screen)

    def move(self):
        # self.body.rear_left.add_vector(Vector(Point(1, 0)))
        # self.body.rear_right.add_vector(Vector(Point(1, 0)))
        # self.body.front_right.add_vector(Vector(Point(1, 0)))
        self.body.front_left.add_vector(Vector(Point(0, 0)))
