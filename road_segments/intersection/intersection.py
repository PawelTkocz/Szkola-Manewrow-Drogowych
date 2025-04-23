from pygame import Surface
from drafter.intersection import IntersectionDrafter
from geometry.direction import Direction
from geometry.shapes.rectangle import AxisAlignedRectangle, Rectangle
from geometry.vector import Point
from road_segments.constants import (
    CONTROL_ELEMENTS_MARGIN,
    LANE_WIDTH,
    LINE_WIDTH,
    ROAD_SEGMENT_SIDE,
)
from road_segments.intersection.schemas import (
    IntersectionColoristics,
    IntersectionParts,
)
from road_segments.road_segment import RoadSegment
from schemas import CardinalDirection, HorizontalDirection

DEFAULT_COLORISTICS: IntersectionColoristics = {
    "lines": "#c3dedd",
    "pavement": "#6e6362",
    "street": "#383838",
}

DEFAULT_TURN_CUVRE = 45


class Intersection(RoadSegment):
    def __init__(
        self,
        colorisitcs: IntersectionColoristics = DEFAULT_COLORISTICS,
        turn_curve: int = DEFAULT_TURN_CUVRE,
    ):
        self.lane_width = LANE_WIDTH
        self.area = AxisAlignedRectangle(
            Point(ROAD_SEGMENT_SIDE / 2, ROAD_SEGMENT_SIDE),
            ROAD_SEGMENT_SIDE,
            ROAD_SEGMENT_SIDE,
        )
        self.turn_curve = turn_curve
        lanes_length = (self.area.length - 2 * self.lane_width) / 2
        self.intersection_parts = self._calculate_intersection_parts()
        pavement_color = colorisitcs["pavement"]

        self.pavements = [
            AxisAlignedRectangle(
                Point(lanes_length / 2, self.area.length),
                lanes_length,
                lanes_length,
                pavement_color,
                border_rear_right_radius=self.turn_curve,
            ),
            AxisAlignedRectangle(
                Point(self.area.width - lanes_length / 2, self.area.length),
                lanes_length,
                lanes_length,
                pavement_color,
                border_rear_left_radius=self.turn_curve,
            ),
            AxisAlignedRectangle(
                Point(lanes_length / 2, lanes_length),
                lanes_length,
                lanes_length,
                pavement_color,
                border_front_right_radius=self.turn_curve,
            ),
            AxisAlignedRectangle(
                Point(self.area.width - lanes_length / 2, lanes_length),
                lanes_length,
                lanes_length,
                pavement_color,
                border_front_left_radius=self.turn_curve,
            ),
        ]
        self.drafter = IntersectionDrafter(
            self.intersection_parts,
            turn_curve,
            self._calculate_default_lines(colorisitcs),
            colorisitcs,
            self.pavements,
        )

    def _calculate_default_lines(
        self, coloristics: IntersectionColoristics
    ) -> list[Rectangle]:
        lines = []
        for side in CardinalDirection:
            outcoming_lane = self.intersection_parts["outcoming_lanes"][side]
            lines.append(
                Rectangle(
                    outcoming_lane.front_left,
                    LINE_WIDTH,
                    outcoming_lane.length,
                    outcoming_lane.direction,
                    coloristics["lines"],
                )
            )
        return lines

    def _calculate_intersection_parts(self) -> IntersectionParts:
        lane_width = self.lane_width
        area = self.area
        street_width = 2 * lane_width
        lanes_length = (area.length - street_width) / 2
        area_center = area.center
        return {
            "intersection_area": AxisAlignedRectangle(
                Point(area_center.x, area_center.y + lane_width),
                street_width,
                street_width,
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

    def draw_road_control_element(
        self, side: CardinalDirection, surface: Surface
    ) -> None:
        pass

    def _get_control_elements_positions(
        self, control_elements: dict[CardinalDirection, list[Surface]]
    ) -> dict[CardinalDirection, list[Point]]:
        def _rect_top_left(side: CardinalDirection, rect: Rectangle) -> Point:
            if side == CardinalDirection.DOWN:
                return rect.front_left
            if side == CardinalDirection.RIGHT:
                return rect.front_right
            if side == CardinalDirection.LEFT:
                return rect.rear_left
            return rect.rear_right

        result: dict[CardinalDirection, list[Point]] = {}
        for side, control_elements_list in control_elements.items():
            lane = self.intersection_parts["incoming_lanes"][side]
            lane_direction = lane.direction
            length_vector = lane_direction.get_negative_of_a_vector()
            width_vector = lane_direction.get_orthogonal_vector(
                HorizontalDirection.RIGHT
            )
            elem_front_left = lane.front_right.add_vector(
                length_vector.copy().scale_to_len(self.turn_curve)
            ).add_vector(width_vector.copy().scale_to_len(CONTROL_ELEMENTS_MARGIN))
            result[side] = []
            for control_element in control_elements_list:
                rect = Rectangle(
                    elem_front_left.add_vector(
                        width_vector.copy().scale_to_len(
                            control_element.get_width() / 2
                        )
                    ),
                    control_element.get_width(),
                    control_element.get_height(),
                    lane_direction,
                )
                result[side].append(_rect_top_left(side, rect))
                elem_front_left = rect.rear_left
        return result
