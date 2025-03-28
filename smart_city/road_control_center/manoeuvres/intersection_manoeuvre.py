from car.model import CarModel
from geometry import Directions
from road_segments.intersection.intersection import Intersection
from smart_city.road_control_center.manoeuvres.manoeuvre import Manoeuvre
from smart_city.road_control_center.manoeuvres.manoeuvre_phase import ManoeuvrePhase
from smart_city.road_control_center.manoeuvres.schemas import (
    IntersectionManoeuvreDescription,
)
from smart_city.road_control_center.manoeuvres.track import (
    TrackPath,
    get_right_angle_turn,
    get_straight_track,
)

vertical = [Directions.UP, Directions.DOWN]
horizontal = [Directions.LEFT, Directions.RIGHT]
directions = [Directions.UP, Directions.RIGHT, Directions.DOWN, Directions.LEFT]
TURN_SHARPNESS = 0.66


def calculate_turn_track(
    intersection: Intersection,
    manoeuvre_description: IntersectionManoeuvreDescription,
    car_length: float,
    turn_direction: Directions,
    turn_margin: float,
    turn_sharpness: float,
) -> TrackPath:
    starting_side = manoeuvre_description["starting_side"]
    ending_side = manoeuvre_description["ending_side"]
    incoming_line = intersection.intersection_parts["incoming_lines"][starting_side]
    start_point = incoming_line.rear_middle
    outcoming_line = intersection.intersection_parts["outcoming_lines"][ending_side]
    end_point = outcoming_line.front_middle.add_vector(
        outcoming_line.direction.scale_to_len(2 * car_length)
    )
    turn_start_point = incoming_line.front_middle.add_vector(
        incoming_line.direction.get_negative_of_a_vector().scale_to_len(turn_margin)
    )
    turn_end_point = outcoming_line.rear_middle.add_vector(
        outcoming_line.direction.scale_to_len(turn_margin)
    )
    incoming_track_path = get_straight_track(start_point, turn_start_point)
    turning_track_path = get_right_angle_turn(
        turn_start_point, turn_end_point, turn_direction, turn_sharpness
    )
    outcoming_track_path = get_straight_track(turn_end_point, end_point)
    return incoming_track_path + turning_track_path + outcoming_track_path


def calculate_left_turn_track_path(
    intersection: Intersection,
    manoeuvre_description: IntersectionManoeuvreDescription,
    car_length: float,
) -> TrackPath:
    return calculate_turn_track(
        intersection,
        manoeuvre_description,
        car_length,
        Directions.LEFT,
        0,
        TURN_SHARPNESS,
    )


def calculate_right_turn_track_path(
    intersection: Intersection,
    manoeuvre_description: IntersectionManoeuvreDescription,
    car_length: float,
) -> TrackPath:
    return calculate_turn_track(
        intersection,
        manoeuvre_description,
        car_length,
        Directions.RIGHT,
        car_length,
        TURN_SHARPNESS,
    )


def calculate_straight_track_path(
    intersection: Intersection,
    manoeuvre_description: IntersectionManoeuvreDescription,
    car_length: float,
) -> TrackPath:
    starting_side = manoeuvre_description["starting_side"]
    ending_side = manoeuvre_description["ending_side"]
    start_point = intersection.intersection_parts["incoming_lines"][
        starting_side
    ].rear_middle
    outcoming_line = intersection.intersection_parts["outcoming_lines"][ending_side]
    end_point = outcoming_line.front_middle.add_vector(
        outcoming_line.direction.scale_to_len(2 * car_length)
    )
    return get_straight_track(start_point, end_point)


def calculate_track_path(
    intersection: Intersection,
    manoeuvre_description: IntersectionManoeuvreDescription,
    car_length: float,
) -> TrackPath:
    starting_side = manoeuvre_description["starting_side"]
    ending_side = manoeuvre_description["ending_side"]
    if (starting_side in vertical and ending_side in vertical) or (
        starting_side in horizontal and ending_side in horizontal
    ):
        return calculate_straight_track_path(
            intersection, manoeuvre_description, car_length
        )

    starting_side_index = directions.index(starting_side)
    if directions[(starting_side_index + 1) % 4] == ending_side:
        return calculate_left_turn_track_path(
            intersection, manoeuvre_description, car_length
        )
    else:
        return calculate_right_turn_track_path(
            intersection, manoeuvre_description, car_length
        )


class IntersectionManoeuvre(Manoeuvre):
    def __init__(
        self,
        model: CarModel,
        intersection: Intersection,
        manoeuvre_description: IntersectionManoeuvreDescription,
    ):
        self.intersection = intersection
        self.manoeuvre_description = manoeuvre_description
        super().__init__(
            [
                ManoeuvrePhase(
                    calculate_track_path(
                        intersection, manoeuvre_description, model.appearance["length"]
                    )
                )
            ]
        )
