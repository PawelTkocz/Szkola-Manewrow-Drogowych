import pygame
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


class SignB20(TrafficSign):
    def __init__(self) -> None:
        super().__init__(TrafficSignName.B20, "sign_B20")


class SignT6aLeft(TrafficSign):
    def __init__(self) -> None:
        super().__init__(TrafficSignName.T6a_LEFT, "sign_T6a")


class SignT6aRight(TrafficSign):
    def __init__(self) -> None:
        super().__init__(TrafficSignName.T6a_RIGHT, "sign_T6a")
        self.original_image = pygame.transform.rotate(self.original_image, 90)
        self.directed_image = self.original_image


class SignT6cLeft(TrafficSign):
    def __init__(self) -> None:
        super().__init__(TrafficSignName.T6c_LEFT, "sign_T6a")
        self.original_image = pygame.transform.rotate(self.original_image, 180)
        self.directed_image = self.original_image


class SignT6cRight(TrafficSign):
    def __init__(self) -> None:
        super().__init__(TrafficSignName.T6c_RIGHT, "sign_T6a")
        self.original_image = pygame.transform.rotate(self.original_image, 270)
        self.directed_image = self.original_image
