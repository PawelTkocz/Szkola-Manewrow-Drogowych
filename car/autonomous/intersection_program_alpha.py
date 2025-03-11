from typing import TypedDict
from car.autonomous.car_simulation import CarSimulation
from car.autonomous.intersection_program import IntersectionProgram
from car.autonomous.program import AvailableManoeuvres, MovementDecision
from car.autonomous.schemas import IntersectionManoeuvreDescription
from car.autonomous.track_follower_alpha import TrackFollowerAlpha
from car.car import LiveCarData, SpeedModifications
from car.model import CarModel
from geometry import Directions
from intersection.intersection import Intersection
from manoeuvres.intersection_manoeuvre import IntersectionManoeuvre
from manoeuvres.manoeuvre_phase import ManoeuvrePhaseEndState


class IntersectionManoeuvreStatus(TypedDict):
    closing_to_intersection: bool
    can_cross_the_intersection: bool


class IntersectionProgramAlpha(IntersectionProgram):
    def __init__(self):
        super().__init__(TrackFollowerAlpha())
        self.max_steps_info_future = 5
        self.manoeuvre_status: IntersectionManoeuvreStatus | None = None

    def prepare_manoeuvre(self, model: CarModel, manoeuvre_description: IntersectionManoeuvreDescription) -> IntersectionManoeuvre:
        intersection = manoeuvre_description['intersection']
        starting_side = manoeuvre_description['starting_side']
        ending_side = manoeuvre_description['ending_side']
        self.current_manoeuvre = IntersectionManoeuvre(model, intersection, starting_side, ending_side)
        self.manoeuvre_status = {
            "closing_to_intersection": True,
            "can_cross_the_intersection": False,
        }
        self.track_follower.set_track(self.current_manoeuvre.current_phase().track.track_path)
        return self.current_manoeuvre

    def make_movement_decision(self, live_car_data: LiveCarData) -> MovementDecision:
        if self.current_manoeuvre is None:
            return {"speed_modification": SpeedModifications.NO_CHANGE, "turn_direction": Directions.FRONT}
        if self.current_manoeuvre.update_current_phase(live_car_data):
            next_manoeuvre_phase = self.current_manoeuvre.current_phase()
            self.track_follower.set_track(next_manoeuvre_phase)
        desired_end_state = self.current_manoeuvre.current_phase().get_desired_end_state()
        movement_decision = self.track_follower.make_movement_decision(live_car_data, desired_end_state)
        return self.validate_movement_decision(movement_decision, live_car_data, desired_end_state)
    
    def validate_movement_decision(self, movement_decision: MovementDecision, live_car_data: LiveCarData, desired_end_state: ManoeuvrePhaseEndState) -> MovementDecision:
        # the movement_decision is what needs to be done to follow the track and meet end state goal
        # modify this movement decision based on intersection state to make sure the crossing will be safe
        # think about considering NO_CHANGE if SPEED_UP doesn't work
        if movement_decision["speed_modification"] == SpeedModifications.BRAKE:
            return movement_decision
        
        if self.manoeuvre_status["closing_to_intersection"]:
            if not self.will_enter_intersection(live_car_data, movement_decision):
                return movement_decision
            self.manoeuvre_status["closing_to_intersection"] = False
        
        if not self.manoeuvre_status["can_cross_the_intersection"]:
            if not self.can_cross_intersection(movement_decision, live_car_data, desired_end_state):
                return {"turn_direction": movement_decision["turn_direction"], "speed_modification": SpeedModifications.BRAKE}
            self.manoeuvre_status["can_cross_the_intersection"] = True
        else:
            return movement_decision

    def can_cross_intersection(self, movement_decision: MovementDecision, live_car_data: LiveCarData, desired_end_state: ManoeuvrePhaseEndState) -> bool:
        # if during my crossing of intesection car with preference would enter too (if it was alone on the street) - violation
        # so no car with preference will enter the intersection area - for all those currently there (we know how they will move)
        # check if you will keep appropriate distance
        car_simulation = CarSimulation(live_car_data)
        intersection = self.current_manoeuvre.intersection
        cars_on_intersection = intersection.get_cars_data()
        simulated_intersection_car = next((car for car in cars_on_intersection if car["live_car_data"].registry_number == car_simulation.registry_number), None)
        if simulated_intersection_car is None:
            return False
        cars_on_intersection.remove(simulated_intersection_car)
        cars_with_preference = [car for car in cars_on_intersection if intersection.has_priority(car, simulated_intersection_car)]
        if not cars_with_preference:
            return True
        
        intersection_incoming_lines = intersection.intersection_parts["incoming_lines"]
        intersection_area = self.current_manoeuvre.intersection.intersection_parts["intersection_area"]  
        cars_with_preference_closing_to_intersection: list[CarSimulation] = []
        cars_with_preference_crossing_intersection: list[CarSimulation] = []

        for car in cars_with_preference:
            car_with_preference_simulation = CarSimulation(car["live_car_data"])
            if car_with_preference_simulation.collides(intersection_incoming_lines[car["starting_side"]]) and not car_with_preference_simulation.collides(intersection_area):
                cars_with_preference_closing_to_intersection.append(car_with_preference_simulation)
            else:
                cars_with_preference_crossing_intersection.append(car_with_preference_simulation)

        # simulate movement of each car until you successfully cross intersection
        # you can't cross the intersection if at any moment one of two things happen:
        # you get to close to one of cars on intersection
        # one of cars closing to intersection enters intersection
        cars_with_preference_simulations = cars_with_preference_crossing_intersection + cars_with_preference_closing_to_intersection
        if self.violates_the_right_of_way(car_simulation, cars_with_preference_simulations):
            return False
        
        while True:
            car_simulation.move(movement_decision=movement_decision)
            for car_with_preference_simulation in cars_with_preference_simulations:
                intersection_program = car_with_preference_simulation.autonomous_driving_program.intersection_program
                track_follower = intersection_program.track_follower
                desired_end_state = intersection_program.current_manoeuvre.current_phase().get_desired_end_state()
                movement_decision = track_follower.make_movement_decision(car_with_preference_simulation.get_live_data(), desired_end_state)
                car_with_preference_simulation.move(movement_decision=movement_decision)
            if self.violates_the_right_of_way(car_simulation, cars_with_preference_simulations):
                return False
            if self.has_crossed_the_intersection(car_simulation, intersection, simulated_intersection_car["ending_side"]):
                return True

    def has_crossed_the_intersection(self, car_simulation: CarSimulation, intersection: Intersection, ending_side: Directions) -> bool:
        intersection_outcoming_lines = intersection.intersection_parts["outcoming_lines"]
        intersection_area = self.current_manoeuvre.intersection.intersection_parts["intersection_area"]
        return car_simulation.collides(intersection_outcoming_lines[ending_side]) and not car_simulation.collides(intersection_area)

    def violates_the_right_of_way(self, car_simulation: CarSimulation, cars_with_preference: list[CarSimulation]) -> bool:
        return any( # and here collides mean enlarged by one car lenght from front and rear
            car_with_preference.collides(car_simulation) for car_with_preference in cars_with_preference
        )

    def will_enter_intersection(self, live_car_data: LiveCarData, movement_decision: MovementDecision, desired_end_state: ManoeuvrePhaseEndState) -> bool:
        car_simulation = CarSimulation(live_car_data)
        car_simulation.move(movement_decision=movement_decision)
        intersection_area = self.current_manoeuvre.intersection.intersection_parts["intersection_area"]
        if car_simulation.collides(intersection_area):
            return True
        for _ in range(self.max_steps_info_future):
            turn_direction = self.track_follower.closest_to_track_turning_policy(car_simulation.get_live_data(), desired_end_state)
            car_simulation.move(movement_decision={"turn_direction": turn_direction, "speed_modification": SpeedModifications.BRAKE})
            if car_simulation.collides(intersection_area):
                return True
            if car_simulation.velocity == 0:
                return False
        return False