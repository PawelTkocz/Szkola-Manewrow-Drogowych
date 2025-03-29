from constants import SCREEN_HEIGHT, SCREEN_WIDTH
from geometry import Direction, Point, Rectangle
from road_segments.intersection.intersection import Intersection
from road_segments.intersection.schemas import IntersectionColors

id = "Intersection_A0"
area = Rectangle(
    Point(SCREEN_WIDTH / 2, SCREEN_HEIGHT),
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    Direction(Point(0, 1)),
)
lane_width = 112
intersection_colors: IntersectionColors = {
    "lines_color": "#c3dedd",
    "pavement_color": "#6e6362",
    "street_color": "#383838",
}
intersection_A0 = Intersection(id, area, lane_width, intersection_colors)
