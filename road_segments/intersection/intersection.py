from pygame import Surface
from drafter.intersection import IntersectionDrafter
from geometry import Direction, Directions, Point, Rectangle
from road_segments.intersection.schemas import IntersectionColors, IntersectionParts


class Intersection:
    def __init__(
        self,
        id: str,
        area: Rectangle,
        lane_width: int,
        intersection_colors: IntersectionColors,
    ):
        self.id = id
        self.lane_width = lane_width
        self.intersection_colors = intersection_colors
        self.area = area.copy()
        self.intersection_parts = self._calculate_intersection_parts()
        self.drafter = IntersectionDrafter(
            self.intersection_parts, self.intersection_colors
        )

    def _calculate_intersection_parts(self) -> IntersectionParts:
        lane_width = self.lane_width
        area = self.area
        area_x = area.front_left.x
        area_y = area.front_left.y
        street_width = 2 * lane_width
        vertical_lanes_length = (area.length - street_width) / 2
        horizontal_lanes_length = (area.width - street_width) / 2
        area_center = area.center
        return {
            "intersection_area": Rectangle(
                Point(area_center.x, area_center.y + lane_width),
                street_width,
                street_width,
                Direction(Point(0, 1)),
            ),
            "incoming_lines": {
                Directions.UP: Rectangle(
                    Point(area_center.x - lane_width / 2, area_center.y + lane_width),
                    lane_width,
                    vertical_lanes_length,
                    Direction(Point(0, -1)),
                ),
                Directions.RIGHT: Rectangle(
                    Point(area_center.x + lane_width, area_center.y + lane_width / 2),
                    lane_width,
                    horizontal_lanes_length,
                    Direction(Point(-1, 0)),
                ),
                Directions.DOWN: Rectangle(
                    Point(area_center.x + lane_width / 2, area_center.y - lane_width),
                    lane_width,
                    vertical_lanes_length,
                    Direction(Point(0, 1)),
                ),
                Directions.LEFT: Rectangle(
                    Point(area_center.x - lane_width, area_center.y - lane_width / 2),
                    lane_width,
                    horizontal_lanes_length,
                    Direction(Point(1, 0)),
                ),
            },
            "outcoming_lines": {
                Directions.UP: Rectangle(
                    Point(area_center.x + lane_width / 2, area_y),
                    lane_width,
                    vertical_lanes_length,
                    Direction(Point(0, 1)),
                ),
                Directions.RIGHT: Rectangle(
                    Point(area_x + area.width, area_center.y - lane_width / 2),
                    lane_width,
                    horizontal_lanes_length,
                    Direction(Point(1, 0)),
                ),
                Directions.DOWN: Rectangle(
                    Point(area_center.x - lane_width / 2, 0),
                    lane_width,
                    vertical_lanes_length,
                    Direction(Point(0, -1)),
                ),
                Directions.LEFT: Rectangle(
                    Point(area_x, area_center.y + lane_width / 2),
                    lane_width,
                    horizontal_lanes_length,
                    Direction(Point(-1, 0)),
                ),
            },
        }

    def draw(self, screen: Surface) -> None:
        self.drafter.draw(screen)
