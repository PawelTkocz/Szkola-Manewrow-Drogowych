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
from traffic_control_elements.traffic_control_element import TrafficControlElement

DEFAULT_COLORISTICS: IntersectionColoristics = {
    "lines": "#c3dedd",
    "pavement": "#6e6362",
    "street": "#383838",
}
DEFAULT_TURN_CUVRE = 45


class Intersection(RoadSegment):
    def __init__(
        self,
        control_elements: dict[CardinalDirection, list[TrafficControlElement]] = {},
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
        self.control_elements = self._set_positions_of_control_elements(
            control_elements
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
        for control_element in self.control_elements:
            control_element.draw(
                screen, scale_factor=scale_factor, screen_y_offset=screen_y_offset
            )

    def _set_positions_of_control_elements(
        self, control_elements: dict[CardinalDirection, list[TrafficControlElement]]
    ) -> list[TrafficControlElement]:
        result = []
        for side, control_elements_list in control_elements.items():
            control_elements_rectangle = self._get_control_elements_rectangle(
                side, control_elements_list
            )
            front_middle = control_elements_rectangle.front_middle
            for control_element in control_elements_list:
                control_element.update_position(
                    front_middle, control_elements_rectangle.direction
                )
                result.append(control_element)
                front_middle = control_element.rear_middle
        return result

    def _get_control_elements_rectangle(
        self,
        side: CardinalDirection,
        control_elements_list: list[TrafficControlElement],
    ) -> Rectangle:
        length = sum(sign.length for sign in control_elements_list)
        width = max(sign.width for sign in control_elements_list)
        lane = self.intersection_parts["incoming_lanes"][side]
        lane_direction = lane.direction
        rect_front_middle = lane.front_right.add_vector(
            lane_direction.get_negative_of_a_vector().scale_to_len(self.turn_curve)
        ).add_vector(
            lane_direction.get_orthogonal_vector(
                HorizontalDirection.RIGHT
            ).scale_to_len(CONTROL_ELEMENTS_MARGIN + width / 2)
        )
        return Rectangle(rect_front_middle, width, length, lane_direction)
