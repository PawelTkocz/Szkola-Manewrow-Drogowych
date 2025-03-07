from typing import TypedDict
from car.autonomous.car_simulation import CarSimulation
from car.autonomous.program import AvailableManoeuvres, MovementDecision
from car.autonomous.track import Track, TrackPath
from car.autonomous.track_follower_alpha import TrackFollowerAlpha
from car.car import LiveCarData, SpeedModifications
from car.model import CarModel
from geometry import Directions, Rectangle
from intersection.intersection import Intersection
from intersection.schemas import CarOnIntersection
from manoeuvres.intersection_manoeuvre import IntersectionManoeruvrePhase, IntersectionManoeuvre


class IntersectionManoeuvreDescription(TypedDict):
    name: AvailableManoeuvres.INTERSECTION
    intersection: Intersection
    starting_side: Directions
    ending_side: Directions


class IntersectionProgram:
    def __init__(self, model: CarModel):
        self.track_follower = TrackFollowerAlpha()
        self.model = model
        self.current_manoeuvre: IntersectionManoeuvre | None = None
        self.max_steps_info_future = 5
        self.intersection_behind = False

    def prepare_manoeuvre(self, manoeuvre_description: IntersectionManoeuvreDescription):
        intersection = manoeuvre_description['intersection']
        starting_side = manoeuvre_description['starting_side']
        ending_side = manoeuvre_description['ending_side']
        self.current_manoeuvre = IntersectionManoeuvre(self.model, intersection, starting_side, ending_side)
        self.track_follower.set_track(self.current_manoeuvre.current_phase().track.track_path)

    def make_movement_decision(self, live_car_data: LiveCarData) -> MovementDecision:
        if self.current_manoeuvre.update_current_phase(live_car_data):
            next_manoeuvre_phase = self.current_manoeuvre.current_phase()
            self.track_follower.set_track(next_manoeuvre_phase)
        if self.current_manoeuvre is None:
            return {"speed_modification": SpeedModifications.NO_CHANGE, "turn_direction": Directions.FRONT}
        desired_end_state = self.current_manoeuvre.current_phase().get_desired_end_state()
        intersection = self.current_manoeuvre.intersection
        movement_decision = self.track_follower.make_movement_decision(live_car_data, desired_end_state)
        if movement_decision["speed_modification"] == SpeedModifications.BRAKE:
            return movement_decision    
        turn_direction = movement_decision["turn_direction"]    
        # check if preference rules will be kept
        speed_modifications = [SpeedModifications.SPEED_UP, SpeedModifications.NO_CHANGE] if movement_decision["speed_modification"] == SpeedModifications.SPEED_UP else [SpeedModifications.NO_CHANGE]
        car_simulation = CarSimulation(live_car_data)
        for speed_modification in speed_modifications:
            start_state = car_simulation.get_current_state()
            car_simulation.move(movement_decision={"speed_modification": speed_modification, "turn_direction": turn_direction})
            will_enter_intersection = self.will_enter_intersection(car_simulation)
            car_simulation.restore_state(start_state)
            if not will_enter_intersection:
                return {"turn_direction": turn_direction, "speed_modification": speed_modification}
            # the car will enter the intersection so we need to check if preferences will be obeyed
            if not self.will_violate_the_right_of_way(car_simulation, intersection):
                return {"turn_direction": turn_direction, "speed_modification": speed_modification}
        return {"turn_direction": movement_decision["turn_direction"], "speed_modification": SpeedModifications.BRAKE}

    def will_violate_the_right_of_way(
        self,
        turning_policy,
        speed_policy,
        cars: list["CarSimulation"],
    ):
        # represent cars with preference as enlarged rectangles - one additional car body in front and rear
        # there can't be situation that car with preference is close to intersection (one car length)
        # no car with preference can get enter the intersection when my car is still on intersection
        # can calculate it only once if the answer is no?
        self_start_state = self.get_state()
        cars_state = [car.get_state() for car in cars]
        collides = False
        entered_non_preference_zone = False
        while True:  # trzeba naprawic
            turn_direction = turning_policy(self)  # better pass state instead of self
            speed_modification = speed_policy(self)
            self.turn(turn_direction)
            self.apply_speed_modification(speed_modification)
            self.move()

            for car in cars:
                turn_direction = turning_policy(
                    car
                )  # better pass state instead of self
                speed_modification = speed_policy(car)
                car.turn(turn_direction)
                car.apply_speed_modification(speed_modification)
                car.move()

            if self.body.collides(non_preference_zone) and any(
                car.body.collides(non_preference_zone) for car in cars
            ):
                collides = True
                break
            if self.body.collides(non_preference_zone):
                entered_non_preference_zone = True
            elif entered_non_preference_zone:
                break
        self.set_state(self_start_state)
        for index, car in enumerate(cars):
            car.set_state(cars_state[index])
        return collides
    
    def can_cross_intersection(self, car_simulation: CarSimulation, intersection: Intersection) -> bool:
        # if during my crossing of intesection car with preference would enter too (if it was alone on the street) - violation
        # so no car with preference will enter the intersection area - for all those currently there (we know how they will move)
        # check if you will keep appropriate distance  
        cars_on_intersection = intersection.get_cars()
        simulated_car = next([car for car in cars_on_intersection if car["live_car_data"].registry_number == car_simulation.registry_number], None)
        if simulated_car is None:
            return False
        cars_on_intersection.remove(simulated_car)
        cars_with_preference = [car for car in cars_on_intersection if intersection.has_priority(car, simulated_car)]
        if not cars_with_preference:
            return True
        
        intersection_incoming_lines = intersection.intersection_parts["incoming_lines"]
        cars_with_preference_closing_to_intersection = [car for car in cars_with_preference if intersection_incoming_lines[car["starting_side"]].is_point_inside(car["live_car_data"].front_middle)]
        cars_with_preference_crossing_intersection = [car for car in cars_with_preference if car not in cars_with_preference_closing_to_intersection]
        # simulate movement of each car until you successfully cross intersection
        # you can't cross the intersection if at any moment one of two things happen:
        # you get to close to one of cars on intersection
        # one of cars closing to intersection enters intersection
        cars_with_preference_simulations = [CarSimulation(car["live_car_data"]) for car in cars_with_preference]
        if self.violates_the_right_of_way(car_simulation, cars_with_preference_simulations):
            return False
        
        simulated_car_start_state = car_simulation.get_current_state()
        cars_with_preference_states = [car.get_current_state() for car in cars_with_preference_simulations]
        collides = False
        entered_non_preference_zone = False
        while True:
            # simulated car is already one step ahead
            movement_decision = self.track_follower.make_movement_decision(car_simulation._live_car_data, None)
            car_simulation.move(movement_decision=movement_decision)

            for car_with_preference_simulation in cars_with_preference_simulations:
                movement_decision = car_with_preference_simulation.autonomous_driving_program.intersection_program.track_follower.make_movement_decision(car_with_preference_simulation._live_car_data, None)
                turn_direction = turning_policy(
                    car
                )
                speed_modification = speed_policy(car)
                car.turn(turn_direction)
                car.apply_speed_modification(speed_modification)
                car.move()

            if self.body.collides(non_preference_zone) and any(
                car.body.collides(non_preference_zone) for car in cars
            ):
                collides = True
                break
            if self.body.collides(non_preference_zone):
                entered_non_preference_zone = True
            elif entered_non_preference_zone:
                break
        self.set_state(self_start_state)
        for index, car in enumerate(cars):
            car.set_state(cars_state[index])
        return collides

    def violates_the_right_of_way(self, car_simulation: CarSimulation, cars_with_preference: list[CarSimulation]) -> bool:
        intersection_area = self.current_manoeuvre.intersection.intersection_parts["intersection_area"]  
        return any( # and here collides mean enlarged by one car lenght from front and rear
            car_with_preference.collides(intersection_area) and car_with_preference.collides(car_simulation) for car_with_preference in cars_with_preference
        )

    def will_enter_intersection(self, car_simulation: CarSimulation) -> bool:
        intersection_area = self.current_manoeuvre.intersection.intersection_parts["intersection_area"]
        if car_simulation.collides(intersection_area):
            return True
        start_state = car_simulation.get_current_state()
        collides = False
        for _ in range(self.max_steps_info_future):
            turn_direction = self.track_follower.closest_to_track_turning_policy(car_simulation._live_car_data)
            car_simulation.move(movement_decision={"turn_direction": turn_direction, "speed_modification": SpeedModifications.BRAKE})
            if car_simulation.collides(intersection_area):
                collides = True
                break
            if car_simulation.velocity == 0:
                break
        car_simulation.restore_state(start_state)
        return collides