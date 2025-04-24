from traffic_control_elements.traffic_signs.traffic_sign import (
    TrafficSign,
    TrafficSignName,
)


class SignA5(TrafficSign):
    def __init__(self) -> None:
        super().__init__(TrafficSignName.A5, "sign_A5")


class SignD1(TrafficSign):
    def __init__(self) -> None:
        super().__init__(TrafficSignName.D1, "sign_D1")


class SignA7(TrafficSign):
    def __init__(self) -> None:
        super().__init__(TrafficSignName.A7, "sign_A7")
