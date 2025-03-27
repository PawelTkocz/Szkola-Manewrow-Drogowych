from car.instruction_controlled_car import MovementInstruction
from smart_city.schemas import LiveCarData
from smart_city.smart_city_car import SmartCityCar


class CarSimulation:
    """
    Class simulating smart city car.
    """

    def __init__(self, live_car_data: LiveCarData):
        """
        Initialize car simulation.
        """
        self.car = SmartCityCar(
            None,
            live_car_data["specification"]["registry_number"],
            live_car_data["specification"]["model"],
            live_car_data["specification"]["color"],
            live_car_data["live_state"]["front_middle"],
            live_car_data["live_state"]["direction"],
            live_car_data["live_state"]["velocity"],
            live_car_data["live_state"]["wheels_direction"],
            live_car_data["live_state"]["high_priority"],
        )

    def get_live_data(self) -> LiveCarData:
        self.car.get_live_data()

    def move(self, movement_instruction: MovementInstruction | None = None) -> None:
        self.car.move(movement_instruction)
