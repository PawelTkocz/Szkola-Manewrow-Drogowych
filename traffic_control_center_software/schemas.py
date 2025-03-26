from typing import TypedDict

from smart_city.schemas import LiveCarData


class EnteringZoneStatus(TypedDict):
    time_to_enter_zone: int
    live_car_data: LiveCarData
