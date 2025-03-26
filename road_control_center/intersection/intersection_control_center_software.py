from typing import TypedDict
from manoeuvres.intersection_manoeuvre import IntersectionManoeuvre
from road_control_center.intersection.schemas import CarOnIntersection
from road_segments.intersection.intersection import Intersection
from traffic_control_center.schemas import LiveCarData
from traffic_control_center_software.car_simulation import CarSimulation
from traffic_control_center_software.track_follower import TrackFollower


class CarOnIntersectionSimulation(TypedDict):
    car: CarOnIntersection
    car_simulation: CarSimulation


def is_car_crossing_intersection(
    live_car_data: LiveCarData,
    manoeuvre_description: IntersectionManoeuvre,
    intersection: Intersection,
) -> bool:
    car_simulation = CarSimulation(live_car_data)
    intersection_area = intersection.intersection_parts["intersection_area"]
    outcoming_lane = intersection.intersection_parts["outcoming_lines"][
        manoeuvre_description["ending_side"]
    ]
    return car_simulation.collides(intersection_area) or car_simulation.collides(
        outcoming_lane
    )


def has_car_crossed_intersection(
    live_car_data: LiveCarData,
    manoeuvre_description: IntersectionManoeuvre,
    intersection: Intersection,
) -> bool:
    car_simulation = CarSimulation(live_car_data)
    intersection_area = intersection.intersection_parts["intersection_area"]
    outcoming_lane = intersection.intersection_parts["outcoming_lines"][
        manoeuvre_description["ending_side"]
    ]
    return not car_simulation.collides(intersection_area) and car_simulation.collides(
        outcoming_lane
    )


def _move_car_simulation(
    car_simulation: CarSimulation, manoeuvre: IntersectionManoeuvre
):
    track = manoeuvre.phases[0].track
    end_state = manoeuvre.phases[0].desired_end_state
    movement_instruction = TrackFollower().get_movement_instruction(
        car_simulation.get_live_data(), track, end_state
    )
    car_simulation.move(movement_instruction=movement_instruction)


def _priority_violation(
    intersection: Intersection,
    car: CarSimulation,
    cars_crossing_intersection: list[CarSimulation],
    cars_closing_to_intersection: list[CarSimulation],
) -> bool:
    intersection_area = intersection.intersection_parts["intersection_area"]
    return any(
        car.collides(intersection_area) for car in cars_closing_to_intersection
    ) or any(car_.collides(car) for car_ in cars_crossing_intersection)


def can_cross_intersection_without_priority_violation(
    car: CarOnIntersection, cars_with_priority: list[CarOnIntersection]
) -> bool:
    cars_crossing_intersection: list[CarOnIntersectionSimulation] = [
        {
            "car": car,
            "car_simulation": CarSimulation(
                car["car_data_transmitter"].get_live_car_data()
            ),
        }
        for car in cars_with_priority
        if is_car_crossing_intersection(car)
    ]
    cars_closing_to_intersection: list[CarOnIntersectionSimulation] = [
        {
            "car": car,
            "car_simulation": CarSimulation(
                car["car_data_transmitter"].get_live_car_data()
            ),
        }
        for car in cars_with_priority
        if not is_car_crossing_intersection(car)
    ]
    car_simulation = CarSimulation(car["car_data_transmitter"].get_live_car_data())
    # if at least one car closing to intersetion would enter the intersection, you CAN'T go
    # if you would get to close to any of cars already on intersection, you CAN'T go
    intersection = car["manoeuvre"].intersection
    while not has_car_crossed_intersection(
        car_simulation.get_live_data(), car["manoeuvre_description"], intersection
    ):
        if _priority_violation(
            intersection,
            car_simulation,
            [car["car_simulation"] for car in cars_crossing_intersection],
            [car["car_simulation"] for car in cars_closing_to_intersection],
        ):
            return False
        _move_car_simulation(car_simulation, car["manoeuvre"])
        for car_on_intersection in (
            cars_crossing_intersection + cars_closing_to_intersection
        ):
            _move_car_simulation(
                car_on_intersection["car_simulation"],
                car_on_intersection["car"]["manoeuvre"],
            )
    return True
