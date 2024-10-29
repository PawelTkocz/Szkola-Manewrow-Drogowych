from Geometry import Direction, Point, Rectangle, Vector
from cars.BasicBrand import BasicBrand
from cars.Brand import Brand


class Car:
    """
    Class representing a car in Cartesian coordinate system
    """

    def __init__(
        self,
        front_left_position: Point,
        direction: Direction = Direction(Point(1, 0)),
        velocity: float = 0,
        reversing: bool = False,
        brand: Brand = BasicBrand(),
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
        # czy screen nie mozna dodac przy init
        corners = [
            self.body.rear_left,
            self.body.rear_right,
            self.body.front_right,
            self.body.front_left,
        ]
        self.brand.draw(corners, screen)

    def move(self):
        self.body.rear_left.add_vector(Vector(Point(1, 0)))
        self.body.rear_right.add_vector(Vector(Point(1, 0)))
        self.body.front_right.add_vector(Vector(Point(1, 0)))
        self.body.front_left.add_vector(Vector(Point(1, 0)))
