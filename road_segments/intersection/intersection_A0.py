from geometry import Direction, Point, Rectangle
from road_segments.intersection.intersection import Intersection


class IntersectionA0(Intersection):
    id = "Intersection_A0"
    area =  Rectangle(Point(300, 0), 600, 600, Direction(Point(0, 1)))
    lane_width = 100

    def __init__(self):
        super().__init__(self.id, self.area, self.lane_width)