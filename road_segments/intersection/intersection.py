from pygame import Surface
from drafter.intersection import IntersectionDrafter
from geometry import Direction, Point, Rectangle
from road_segments.constants import LANE_WIDTH, ROAD_SEGMENT_SIDE
from road_segments.intersection.schemas import (
    IntersectionColoristics,
    IntersectionParts,
)
from road_segments.road_segment import RoadSegment
from schemas import CardinalDirection
# mozna dodac linie na skrzozowaniu
# plus znaki


class Intersection(RoadSegment):
    def __init__(
        self,
        id: str,
        colorisitcs: IntersectionColoristics,
    ):
        self.id = id
        self.lane_width = LANE_WIDTH
        self.turn_curve = 90
        self.colorisitcs = colorisitcs
        self.area = Rectangle(
            Point(ROAD_SEGMENT_SIDE / 2, ROAD_SEGMENT_SIDE),
            ROAD_SEGMENT_SIDE,
            ROAD_SEGMENT_SIDE,
            Direction(Point(0, 1)),
        )
        self.intersection_parts = self._calculate_intersection_parts()
        self.drafter = IntersectionDrafter(self.intersection_parts, self.colorisitcs)

    def _calculate_intersection_parts(self) -> IntersectionParts:
        lane_width = self.lane_width
        area = self.area
        street_width = 2 * lane_width
        lanes_length = (area.length - street_width) / 2
        area_center = area.center
        return {
            "intersection_area": Rectangle(
                Point(area_center.x, area_center.y + lane_width),
                street_width,
                street_width,
                Direction(Point(0, 1)),
            ),
            "incoming_lanes": {
                CardinalDirection.UP: Rectangle(
                    Point(area_center.x - lane_width / 2, area_center.y + lane_width),
                    lane_width,
                    lanes_length,
                    Direction(Point(0, -1)),
                ),
                CardinalDirection.RIGHT: Rectangle(
                    Point(area_center.x + lane_width, area_center.y + lane_width / 2),
                    lane_width,
                    lanes_length,
                    Direction(Point(-1, 0)),
                ),
                CardinalDirection.DOWN: Rectangle(
                    Point(area_center.x + lane_width / 2, area_center.y - lane_width),
                    lane_width,
                    lanes_length,
                    Direction(Point(0, 1)),
                ),
                CardinalDirection.LEFT: Rectangle(
                    Point(area_center.x - lane_width, area_center.y - lane_width / 2),
                    lane_width,
                    lanes_length,
                    Direction(Point(1, 0)),
                ),
            },
            "outcoming_lanes": {
                CardinalDirection.UP: Rectangle(
                    Point(area_center.x + lane_width / 2, area.length),
                    lane_width,
                    lanes_length,
                    Direction(Point(0, 1)),
                ),
                CardinalDirection.RIGHT: Rectangle(
                    Point(area.width, area_center.y - lane_width / 2),
                    lane_width,
                    lanes_length,
                    Direction(Point(1, 0)),
                ),
                CardinalDirection.DOWN: Rectangle(
                    Point(area_center.x - lane_width / 2, 0),
                    lane_width,
                    lanes_length,
                    Direction(Point(0, -1)),
                ),
                CardinalDirection.LEFT: Rectangle(
                    Point(0, area_center.y + lane_width / 2),
                    lane_width,
                    lanes_length,
                    Direction(Point(-1, 0)),
                ),
            },
        }

    def draw(
        self, screen: Surface, *, scale_factor: float = 1, screen_y_offset: int = 0
    ) -> None:
        self.drafter.draw(
            screen, scale_factor=scale_factor, screen_y_offset=screen_y_offset
        )
