from geometry import Direction, Point, Rectangle
from road_segments.intersection.intersection import Intersection
from road_segments.intersection.schemas import IntersectionColors


class IntersectionA0(Intersection):
    id = "Intersection_A0"
    area = Rectangle(Point(300, 0), 600, 600, Direction(Point(0, 1)))
    lane_width = 112
    intersection_colors: IntersectionColors = {
        "lines_color": "#c3dedd",
        "pavement_color": "#6e6362",
        "street_color": "#383838",
    }

    def __init__(self) -> None:
        super().__init__(self.id, self.area, self.lane_width, self.intersection_colors)


id = "Intersection_A0"
area = Rectangle(Point(300, 0), 600, 600, Direction(Point(0, 1)))
lane_width = 112
intersection_colors: IntersectionColors = {
    "lines_color": "#c3dedd",
    "pavement_color": "#6e6362",
    "street_color": "#383838",
}
intersection_A0 = Intersection(id, area, lane_width, intersection_colors)
