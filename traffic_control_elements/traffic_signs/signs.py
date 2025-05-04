from traffic_control_elements.traffic_signs.traffic_sign import (
    TrafficSign,
    TrafficSignName,
)


class SignA5(TrafficSign):
    def __init__(self) -> None:
        super().__init__(TrafficSignName.A5, "sign_A5.png")


class SignD1(TrafficSign):
    def __init__(self) -> None:
        super().__init__(TrafficSignName.D1, "sign_D1.png")


class SignA7(TrafficSign):
    def __init__(self) -> None:
        super().__init__(TrafficSignName.A7, "sign_A7.png")


class SignB20(TrafficSign):
    def __init__(self) -> None:
        super().__init__(TrafficSignName.B20, "sign_B20.png")


class SignT6aLeft(TrafficSign):
    def __init__(self) -> None:
        super().__init__(TrafficSignName.T6a_LEFT, "sign_T6a_left.png")


class SignT6aRight(TrafficSign):
    def __init__(self) -> None:
        super().__init__(TrafficSignName.T6a_RIGHT, "sign_T6a_right.png")


class SignT6cLeft(TrafficSign):
    def __init__(self) -> None:
        super().__init__(TrafficSignName.T6c_LEFT, "sign_T6c_left.png")


class SignT6cRight(TrafficSign):
    def __init__(self) -> None:
        super().__init__(TrafficSignName.T6c_RIGHT, "sign_T6c_right.png")
