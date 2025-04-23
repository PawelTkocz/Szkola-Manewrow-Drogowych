from traffic_control_elements.traffic_signs.traffic_sign import (
    TrafficSign,
    TrafficSignName,
)


class SignA5(TrafficSign):
    def __init__(self) -> None:
        super().__init__(TrafficSignName.A5, "sign_A5")
