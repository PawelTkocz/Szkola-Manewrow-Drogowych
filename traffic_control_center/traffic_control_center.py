# in the future road_control_center can be list of centers, and after each frame
# the traffic control center should reassign car to road control centers based on 
# car position. 

from car.autonomous_car import CarDataTransmitter
from road_control_center.intersection.intersection_A0 import IntersectionA0ControlCenter
from road_control_center.road_control_center import RoadControlCenter


class TrafficControlCenter:
    def __init__(self, road_control_center: RoadControlCenter):
        self._road_control_center = road_control_center
        self._time = 0

    def pair_with_car_data_transmitter(self, car_data_transmitter: CarDataTransmitter):
        self._road_control_center.add_car(car_data_transmitter)
        car_data_transmitter.set_traffic_control_center(self)

    def send_movement_instructions(self):
        self._time += 1
        self._road_control_center.update_time()
        self._road_control_center.send_movement_instructions()

traffic_control_center = TrafficControlCenter(IntersectionA0ControlCenter())

    