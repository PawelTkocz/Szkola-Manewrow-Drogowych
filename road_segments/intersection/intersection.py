from geometry.direction import Direction
from geometry.shapes.rectangle import AxisAlignedRectangle, Rectangle
from geometry.vector import Point
from road_elements_drafter import RoadElementsDrafter
from road_segments.constants import (
    CONTROL_ELEMENTS_DISTANCE_FROM_ROAD,
    LANE_WIDTH,
    LINE_WIDTH,
    ROAD_SEGMENT_SIDE,
)
from road_segments.intersection.schemas import (
    IntersectionColors,
    IntersectionComponents,
)
from road_segments.road_segment import RoadSegment
from schemas import CardinalDirection, HorizontalDirection
from traffic_control_elements.traffic_control_element import TrafficControlElement
from traffic_control_elements.traffic_lights.intersection.intersection_traffic_lights import (
    IntersectionTrafficLights,
)
from traffic_control_elements.traffic_lights.traffic_lights import TrafficLights
from traffic_control_elements.traffic_signs.traffic_sign import TrafficSign

DEFAULT_COLORS: IntersectionColors = {
    "lines": "#c3dedd",
    "pavement": "#6e6362",
    "street": "#383838",
}
DEFAULT_PAVEMENT_CORNER_RADIUS = 45


class Intersection(RoadSegment):
    def __init__(
        self,
        *,
        traffic_lights: IntersectionTrafficLights | None = None,
        traffic_signs: dict[CardinalDirection, list[TrafficSign]] | None = None,
        colors: IntersectionColors = DEFAULT_COLORS,
        pavement_corner_radius: int = DEFAULT_PAVEMENT_CORNER_RADIUS,
    ):
        self._area = AxisAlignedRectangle(
            Point(ROAD_SEGMENT_SIDE / 2, ROAD_SEGMENT_SIDE),
            ROAD_SEGMENT_SIDE,
            ROAD_SEGMENT_SIDE,
            color=colors["street"],
        )
        self.pavement_corner_radius = pavement_corner_radius
        self.components = self._compute_components()
        self.pavements = self._compute_pavements(colors)
        self.lines = self._compute_lines(colors)
        self.traffic_lights = traffic_lights
        self.control_elements = self._set_positions_of_control_elements(
            traffic_lights.get_lights() if traffic_lights else {}, traffic_signs or {}
        )

    @property
    def area(self) -> AxisAlignedRectangle:
        return self._area

    def _compute_pavements(
        self, colors: IntersectionColors
    ) -> list[AxisAlignedRectangle]:
        lanes_length = (self._area.length - 2 * LANE_WIDTH) / 2
        pavement_color = colors["pavement"]
        return [
            AxisAlignedRectangle(
                Point(lanes_length / 2, self._area.length),
                lanes_length,
                lanes_length,
                pavement_color,
                border_rear_right_radius=self.pavement_corner_radius,
            ),
            AxisAlignedRectangle(
                Point(self._area.width - lanes_length / 2, self._area.length),
                lanes_length,
                lanes_length,
                pavement_color,
                border_rear_left_radius=self.pavement_corner_radius,
            ),
            AxisAlignedRectangle(
                Point(lanes_length / 2, lanes_length),
                lanes_length,
                lanes_length,
                pavement_color,
                border_front_right_radius=self.pavement_corner_radius,
            ),
            AxisAlignedRectangle(
                Point(self._area.width - lanes_length / 2, lanes_length),
                lanes_length,
                lanes_length,
                pavement_color,
                border_front_left_radius=self.pavement_corner_radius,
            ),
        ]

    def _compute_lines(self, colors: IntersectionColors) -> list[Rectangle]:
        lines = []
        for side in CardinalDirection:
            outcoming_lane = self.components["outcoming_lanes"][side]
            lines.append(
                Rectangle(
                    outcoming_lane.front_left,
                    LINE_WIDTH,
                    outcoming_lane.length,
                    outcoming_lane.direction,
                    colors["lines"],
                )
            )
        return lines

    def _compute_components(self) -> IntersectionComponents:
        area = self._area
        street_width = 2 * LANE_WIDTH
        lanes_length = (area.length - street_width) / 2
        area_center = area.center
        return {
            "intersection_area": Rectangle(
                Point(area_center.x, area_center.y + LANE_WIDTH),
                street_width,
                street_width,
                Direction(Point(0, 1)),
            ),
            "incoming_lanes": {
                CardinalDirection.UP: Rectangle(
                    Point(area_center.x - LANE_WIDTH / 2, area_center.y + LANE_WIDTH),
                    LANE_WIDTH,
                    lanes_length,
                    Direction(Point(0, -1)),
                ),
                CardinalDirection.RIGHT: Rectangle(
                    Point(area_center.x + LANE_WIDTH, area_center.y + LANE_WIDTH / 2),
                    LANE_WIDTH,
                    lanes_length,
                    Direction(Point(-1, 0)),
                ),
                CardinalDirection.DOWN: Rectangle(
                    Point(area_center.x + LANE_WIDTH / 2, area_center.y - LANE_WIDTH),
                    LANE_WIDTH,
                    lanes_length,
                    Direction(Point(0, 1)),
                ),
                CardinalDirection.LEFT: Rectangle(
                    Point(area_center.x - LANE_WIDTH, area_center.y - LANE_WIDTH / 2),
                    LANE_WIDTH,
                    lanes_length,
                    Direction(Point(1, 0)),
                ),
            },
            "outcoming_lanes": {
                CardinalDirection.UP: Rectangle(
                    Point(area_center.x + LANE_WIDTH / 2, area.length),
                    LANE_WIDTH,
                    lanes_length,
                    Direction(Point(0, 1)),
                ),
                CardinalDirection.RIGHT: Rectangle(
                    Point(area.width, area_center.y - LANE_WIDTH / 2),
                    LANE_WIDTH,
                    lanes_length,
                    Direction(Point(1, 0)),
                ),
                CardinalDirection.DOWN: Rectangle(
                    Point(area_center.x - LANE_WIDTH / 2, 0),
                    LANE_WIDTH,
                    lanes_length,
                    Direction(Point(0, -1)),
                ),
                CardinalDirection.LEFT: Rectangle(
                    Point(0, area_center.y + LANE_WIDTH / 2),
                    LANE_WIDTH,
                    lanes_length,
                    Direction(Point(-1, 0)),
                ),
            },
        }

    def draw(self, road_elements_drafter: RoadElementsDrafter) -> None:
        road_elements_drafter.draw_rectangle(self.area)
        for pavement in self.pavements:
            road_elements_drafter.draw_rectangle(pavement)
        for line in self.lines:
            road_elements_drafter.draw_polygon(line)
        for control_element in self.control_elements:
            control_element.draw_on_road(road_elements_drafter)

    def _set_positions_of_control_elements(
        self,
        traffic_lights: dict[CardinalDirection, TrafficLights],
        traffic_signs: dict[CardinalDirection, list[TrafficSign]],
    ) -> list[TrafficControlElement]:
        control_elements = []
        for side in CardinalDirection:
            control_elements_list: list[TrafficControlElement] = []
            if side in traffic_lights:
                control_elements_list.append(traffic_lights[side])
            if side in traffic_signs:
                control_elements_list.extend(traffic_signs[side])
            control_elements_zone = self._compute_control_elements_zone(
                side, control_elements_list
            )
            front_middle = control_elements_zone.front_middle
            for control_element in control_elements_list:
                control_element.update_position(
                    front_middle, control_elements_zone.direction
                )
                control_elements.append(control_element)
                front_middle = control_element.rear_middle
        return control_elements

    def _compute_control_elements_zone(
        self,
        side: CardinalDirection,
        control_elements_list: list[TrafficControlElement],
    ) -> Rectangle:
        length = sum(
            control_element.length for control_element in control_elements_list
        )
        width = max(control_element.width for control_element in control_elements_list)
        incoming_lane = self.components["incoming_lanes"][side]
        lane_direction = incoming_lane.direction
        zone_front_middle = incoming_lane.front_right.add_vector(
            lane_direction.get_negative_of_a_vector().scale_to_len(
                self.pavement_corner_radius
            )
        ).add_vector(
            lane_direction.get_orthogonal_vector(
                HorizontalDirection.RIGHT
            ).scale_to_len(CONTROL_ELEMENTS_DISTANCE_FROM_ROAD + width / 2)
        )
        return Rectangle(zone_front_middle, width, length, lane_direction)

    def tick(self) -> None:
        if self.traffic_lights:
            self.traffic_lights.tick()
