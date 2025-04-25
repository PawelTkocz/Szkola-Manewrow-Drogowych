import pygame
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
        super().__init__(TrafficSignName.T6a_LEFT, "sign_T6a.png")


class SignT6aRight(TrafficSign):
    def __init__(self) -> None:
        super().__init__(TrafficSignName.T6a_RIGHT, "sign_T6a.png")
        self.original_state_images = [
            pygame.transform.rotate(self.original_state_images[0], 90)
        ]
        self.rotated_state_images = self.original_state_images


class SignT6cLeft(TrafficSign):
    def __init__(self) -> None:
        super().__init__(TrafficSignName.T6c_LEFT, "sign_T6a.png")
        self.original_state_images = [
            pygame.transform.rotate(self.original_state_images[0], 180)
        ]
        self.rotated_state_images = self.original_state_images


class SignT6cRight(TrafficSign):
    def __init__(self) -> None:
        super().__init__(TrafficSignName.T6c_RIGHT, "sign_T6a.png")
        self.original_state_images = [
            pygame.transform.rotate(self.original_state_images[0], 270)
        ]
        self.rotated_state_images = self.original_state_images
