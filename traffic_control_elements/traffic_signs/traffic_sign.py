from enum import Enum
from traffic_control_elements.traffic_control_element import TrafficControlElement


class TrafficSignName(Enum):
    A5 = "A5"
    D1 = "D1"
    A7 = "A7"
    B20 = "B20"
    T6a_LEFT = "T6a_LEFT"
    T6a_RIGHT = "T6a_RIGHT"
    T6c_LEFT = "T6c_LEFT"
    T6c_RIGHT = "T6c_RIGHT"


SIGN_WIDTH = 50


class TrafficSign(TrafficControlElement):
    def __init__(
        self,
        name: TrafficSignName,
        image_file_name: str,
    ) -> None:
        super().__init__([image_file_name], SIGN_WIDTH)
        self.name = name


# move scale factor and y offset to some global variables
