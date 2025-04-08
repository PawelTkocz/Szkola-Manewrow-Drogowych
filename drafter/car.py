from pygame import Surface
from car.model import CarModel
from car.schemas import CarPartPosition, CarPointPosition
from drafter.drafter_base import DrafterBase
from geometry import Point, Rectangle
from schemas import HorizontalDirection


class CarDrafter(DrafterBase):
    """
    Class responsible for drawing car on the screen.
    """

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
        scale=1,
        screen_y_offset: int = 0,
    ) -> None:
        corners = self._get_car_part_corners(car_body, car_part_position)
        self.draw_polygon(
            screen, color, corners, scale=scale, screen_y_offset=screen_y_offset
        )

    def _draw_body(
        self,
        car_model: CarModel,
        car_body: Rectangle,
        color: str,
        screen: Surface,
        bumpers_color: str = "black",
        *,
        scale=1,
        screen_y_offset: int = 0,
    ) -> None:
        # Draw bumpers
        self.draw_polygon(
            screen,
            bumpers_color,
            car_body.corners_list,
            scale=scale,
            screen_y_offset=screen_y_offset,
        )

        # Draw the car shell
        model_appearance = car_model.appearance
        self._draw_car_part(
            car_body,
            model_appearance["shell"],
            color,
            screen,
            scale=scale,
            screen_y_offset=screen_y_offset,
        )

    def _draw_lights(
        self,
        car_model: CarModel,
        car_body: Rectangle,
        turn_signals_lights_on: dict[HorizontalDirection, bool],
        screen: Surface,
        no_turn_signal_color: str = "#fbee0f",
        turn_signal_color: str = "#F86F15",
        *,
        scale: float = 1,
        screen_y_offset: int = 0,
    ) -> None:
        def _get_light_color(light_side: HorizontalDirection) -> str:
            if turn_signals_lights_on[light_side]:
                return turn_signal_color
            return no_turn_signal_color

        model_appearance = car_model.appearance
        front_lights_appearance = model_appearance["front_lights"]
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
                scale=scale,
                screen_y_offset=screen_y_offset,
            )

    def _draw_side_mirrors(
        self,
        car_model: CarModel,
        car_body: Rectangle,
        screen: Surface,
        color: str = "black",
        *,
        scale=1,
        screen_y_offset: int = 0,
    ) -> None:
        model_appearance = car_model.appearance
        side_mirrors_appearance = model_appearance["side_mirrors"]
        for mirrors_positions in [
            side_mirrors_appearance["left"],
            side_mirrors_appearance["right"],
        ]:
            self._draw_car_part(
                car_body,
                mirrors_positions,
                color,
                screen,
                scale=scale,
                screen_y_offset=screen_y_offset,
            )

    def _draw_windows(
        self,
        car_model: CarModel,
        car_body: Rectangle,
        screen: Surface,
        color: str = "black",
        *,
        scale=1,
        screen_y_offset: int = 0,
    ) -> None:
        model_appearance = car_model.appearance
        windows_appearance = model_appearance["windows"]
        for windows_positions in [
            windows_appearance["front"],
            windows_appearance["rear"],
            windows_appearance["left"],
            windows_appearance["right"],
        ]:
            self._draw_car_part(
                car_body,
                windows_positions,
                color,
                screen,
                scale=scale,
                screen_y_offset=screen_y_offset,
            )

    def _draw_wheels(
        self,
        car_model: CarModel,
        car_body: Rectangle,
        screen: Surface,
        wheels_angle: float,
        color: str = "#262626",
        *,
        scale=1,
        screen_y_offset: int = 0,
    ) -> None:
        model_wheels_positions = car_model.wheels_positions
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
            self.draw_polygon(
                screen,
                color,
                rotated_wheel_corners,
                scale=scale,
                screen_y_offset=screen_y_offset,
            )

    def draw(
        self,
        model: CarModel,
        color: str,
        car_body: Rectangle,
        wheels_angle: float,
        turn_signals_lights_on: dict[HorizontalDirection, bool],
        screen: Surface,
        *,
        scale=1,
        screen_y_offset: int = 0,
    ) -> None:
        """
        Draw the car on the screen.

        :param car_body: Rectangle representing position of the car body
        :wheels_angle: angle of the wheels turn
        :param screen: pygame screen to draw the car on
        """
        self._draw_wheels(
            model,
            car_body,
            screen,
            wheels_angle,
            scale=scale,
            screen_y_offset=screen_y_offset,
        )
        self._draw_body(
            model, car_body, color, screen, scale=scale, screen_y_offset=screen_y_offset
        )
        self._draw_lights(
            model,
            car_body,
            turn_signals_lights_on,
            screen,
            scale=scale,
            screen_y_offset=screen_y_offset,
        )
        self._draw_side_mirrors(
            model, car_body, screen, scale=scale, screen_y_offset=screen_y_offset
        )
        self._draw_windows(
            model, car_body, screen, scale=scale, screen_y_offset=screen_y_offset
        )
