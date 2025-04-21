from pygame import Surface
from car.model import CarModel
from car.schemas import CarColoristics, CarPartPosition, CarPointPosition
from drafter.utils import draw_polygon
from geometry.vector import Point
from geometry.rectangle import Rectangle
from schemas import HorizontalDirection


class CarDrafter:
    """
    Class responsible for drawing car on the screen.
    """

    def __init__(self, car_model: CarModel, coloristics: CarColoristics) -> None:
        self.model_appearance = car_model.appearance
        self.wheels_positions = car_model.wheels_positions
        self.coloristics = coloristics

    def _get_car_point_position(
        self, car_body: Rectangle, position: CarPointPosition
    ) -> Point:
        """
        Based on car point position, return current point position.
        """
        length_vector = car_body.direction
        width_vector = car_body.direction.get_orthogonal_vector(
            HorizontalDirection.RIGHT
        )
        length_position_vector = length_vector.copy().scale_to_len(position["y"])
        width_position_vector = width_vector.copy().scale_to_len(position["x"])
        return (
            car_body.front_middle.copy()
            .add_vector(length_position_vector)
            .add_vector(width_position_vector)
        )

    def _get_car_part_corners(
        self, car_body: Rectangle, car_part_position: CarPartPosition
    ) -> list[Point]:
        """
        Based on car part position and current car position, return current car part corners.
        """
        return [
            self._get_car_point_position(car_body, corner_position)
            for corner_position in car_part_position
        ]

    def _draw_car_part(
        self,
        car_body: Rectangle,
        car_part_position: CarPartPosition,
        color: str,
        screen: Surface,
        *,
        scale_factor: float = 1,
        screen_y_offset: int = 0,
    ) -> None:
        corners = self._get_car_part_corners(car_body, car_part_position)
        draw_polygon(
            screen,
            color,
            corners,
            scale_factor=scale_factor,
            screen_y_offset=screen_y_offset,
        )

    def _draw_body(
        self,
        car_body: Rectangle,
        screen: Surface,
        *,
        scale_factor: float = 1,
        screen_y_offset: int = 0,
    ) -> None:
        # Draw bumpers
        draw_polygon(
            screen,
            self.coloristics["bumpers"],
            car_body.corners_list,
            scale_factor=scale_factor,
            screen_y_offset=screen_y_offset,
        )

        # Draw the car shell
        self._draw_car_part(
            car_body,
            self.model_appearance["shell"],
            self.coloristics["shell"],
            screen,
            scale_factor=scale_factor,
            screen_y_offset=screen_y_offset,
        )

    def _draw_lights(
        self,
        car_body: Rectangle,
        turn_signals_lights_on: dict[HorizontalDirection, bool],
        screen: Surface,
        *,
        scale_factor: float = 1,
        screen_y_offset: int = 0,
    ) -> None:
        def _get_light_color(light_side: HorizontalDirection) -> str:
            if turn_signals_lights_on[light_side]:
                return self.coloristics["turn_signals"]
            return self.coloristics["lights"]

        front_lights_appearance = self.model_appearance["front_lights"]
        for lights_positions, color in [
            (
                front_lights_appearance["left"],
                _get_light_color(HorizontalDirection.LEFT),
            ),
            (
                front_lights_appearance["right"],
                _get_light_color(HorizontalDirection.RIGHT),
            ),
        ]:
            self._draw_car_part(
                car_body,
                lights_positions,
                color,
                screen,
                scale_factor=scale_factor,
                screen_y_offset=screen_y_offset,
            )

    def _draw_side_mirrors(
        self,
        car_body: Rectangle,
        screen: Surface,
        *,
        scale_factor: float = 1,
        screen_y_offset: int = 0,
    ) -> None:
        side_mirrors_appearance = self.model_appearance["side_mirrors"]
        for mirrors_positions in [
            side_mirrors_appearance["left"],
            side_mirrors_appearance["right"],
        ]:
            self._draw_car_part(
                car_body,
                mirrors_positions,
                self.coloristics["side_mirrors"],
                screen,
                scale_factor=scale_factor,
                screen_y_offset=screen_y_offset,
            )

    def _draw_windows(
        self,
        car_body: Rectangle,
        screen: Surface,
        *,
        scale_factor: float = 1,
        screen_y_offset: int = 0,
    ) -> None:
        windows_appearance = self.model_appearance["windows"]
        for windows_positions in [
            windows_appearance["front"],
            windows_appearance["rear"],
            windows_appearance["left"],
            windows_appearance["right"],
        ]:
            self._draw_car_part(
                car_body,
                windows_positions,
                self.coloristics["windows"],
                screen,
                scale_factor=scale_factor,
                screen_y_offset=screen_y_offset,
            )

    def _draw_wheels(
        self,
        car_body: Rectangle,
        screen: Surface,
        wheels_angle: float,
        *,
        scale_factor: float = 1,
        screen_y_offset: int = 0,
    ) -> None:
        model_wheels_positions = self.wheels_positions
        for wheels_positions in [
            model_wheels_positions["left"],
            model_wheels_positions["right"],
        ]:
            wheel_corners = self._get_car_part_corners(
                car_body, wheels_positions["corners"]
            )
            wheel_middle = self._get_car_point_position(
                car_body, wheels_positions["middle"]
            )
            rotated_wheel_corners = [
                corner.rotate_over_point(wheel_middle, wheels_angle)
                for corner in wheel_corners
            ]
            draw_polygon(
                screen,
                self.coloristics["wheels"],
                rotated_wheel_corners,
                scale_factor=scale_factor,
                screen_y_offset=screen_y_offset,
            )

    def draw(
        self,
        car_body: Rectangle,
        wheels_angle: float,
        turn_signals_lights_on: dict[HorizontalDirection, bool],
        screen: Surface,
        *,
        scale_factor: float = 1,
        screen_y_offset: int = 0,
    ) -> None:
        self._draw_wheels(
            car_body,
            screen,
            wheels_angle,
            scale_factor=scale_factor,
            screen_y_offset=screen_y_offset,
        )
        self._draw_body(
            car_body,
            screen,
            scale_factor=scale_factor,
            screen_y_offset=screen_y_offset,
        )
        self._draw_lights(
            car_body,
            turn_signals_lights_on,
            screen,
            scale_factor=scale_factor,
            screen_y_offset=screen_y_offset,
        )
        self._draw_side_mirrors(
            car_body,
            screen,
            scale_factor=scale_factor,
            screen_y_offset=screen_y_offset,
        )
        self._draw_windows(
            car_body,
            screen,
            scale_factor=scale_factor,
            screen_y_offset=screen_y_offset,
        )
