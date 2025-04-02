import math
from pygame import Surface
from geometry import Circle, Direction, Directions, Point, Rectangle
from road_segments.roundabout.schemas import RoundaboutColors, RoundaboutParts


# make lane width global
class Roundabout:
    def __init__(
        self,
        id: str,
        area: Rectangle,
        lane_width: int,
        roundabout_radius: int,
        central_island_radius: int,
        roundabout_colors: RoundaboutColors,
    ):
        self.id = id
        self.lane_width = lane_width
        self.roundabout_radius = roundabout_radius
        self.central_island_radius = central_island_radius
        self.roundabout_colors = roundabout_colors
        self.area = area.copy()
        self.intersection_parts = self._calculate_intersection_parts()
        # self.drafter = RoundaboutDrafter(
        #     self.intersection_parts, self.roundabout_colors
        # )

    def _calculate_intersection_parts(self) -> RoundaboutParts:
        lane_width = self.lane_width
        area = self.area
        area_x = area.front_left.x
        area_y = area.front_left.y

        x = math.sqrt(self.roundabout_radius**2 - lane_width**2)
        vertical_lanes_length = (area.length - 2 * x) / 2
        horizontal_lanes_length = (area.width - 2 * x) / 2
        area_center = area.center
        return {
            "roundabout_area": Circle(area_center, self.roundabout_radius),
            "central_island": Circle(area_center, self.central_island_radius),
            "incoming_lines": {
                Directions.UP: Rectangle(
                    Point(area_center.x - lane_width / 2, area_center.y + x),
                    lane_width,
                    vertical_lanes_length,
                    Direction(Point(0, -1)),
                ),
                Directions.RIGHT: Rectangle(
                    Point(area_center.x + x, area_center.y + lane_width / 2),
                    lane_width,
                    horizontal_lanes_length,
                    Direction(Point(-1, 0)),
                ),
                Directions.DOWN: Rectangle(
                    Point(area_center.x + lane_width / 2, area_center.y - x),
                    lane_width,
                    vertical_lanes_length,
                    Direction(Point(0, 1)),
                ),
                Directions.LEFT: Rectangle(
                    Point(area_center.x - x, area_center.y - lane_width / 2),
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
        pass
        # self.drafter.draw(screen)
