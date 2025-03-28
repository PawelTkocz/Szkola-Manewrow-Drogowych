from pygame import Surface
from animations.animations_generators.intersection.go_straight import (
    IntersectionGoStraightAnimation,
)
from animations.animations_generators.intersection.turn_left import (
    IntersectionTurnLeftAnimation,
)
from animations.animations_generators.intersection.turn_right import (
    IntersectionTurnRightAnimation,
)
from animations.animations_menus.constants import (
    INTERSECTION_MENU_OPTIONS_COLUMNS_NUMBER,
    INTERSECTION_MENU_TITLE,
    MENU_OPTIONS_IMAGE_SIDE,
    MENU_OPTIONS_X_SPACING,
    MENU_OPTIONS_Y_SPACING,
    MENU_TITLE_TOP_OFFSET,
)
from animations.animations_menus.options_menu import OptionsMenu
from constants import BACKGROUND_COLOR, SCREEN_HEIGHT, SCREEN_WIDTH

from state import State


class IntersectionManoeuvresMenu(State):
    def __init__(self, previous_state: State) -> None:
        super().__init__(previous_state=previous_state)
        self.options_menu = OptionsMenu(
            INTERSECTION_MENU_TITLE,
            INTERSECTION_MENU_OPTIONS_COLUMNS_NUMBER,
            SCREEN_HEIGHT,
            SCREEN_WIDTH,
            MENU_TITLE_TOP_OFFSET,
            MENU_OPTIONS_X_SPACING,
            MENU_OPTIONS_Y_SPACING,
            MENU_OPTIONS_IMAGE_SIDE,
        )
        self.options_menu.add_option_item(
            {
                "title": "Turn right",
                "image_path": "animations/animations_menus/screenshots/screenshot1.png",
                "on_click_state": IntersectionTurnRightAnimation(self),
            }
        )
        self.options_menu.add_option_item(
            {
                "title": "Go straight",
                "image_path": "animations/animations_menus/screenshots/screenshot1.png",
                "on_click_state": IntersectionGoStraightAnimation(self),
            }
        )
        self.options_menu.add_option_item(
            {
                "title": "Turn left",
                "image_path": "animations/animations_menus/screenshots/screenshot1.png",
                "on_click_state": IntersectionTurnLeftAnimation(self),
            }
        )

    def render_frame(self, screen: Surface) -> None:
        screen.fill(BACKGROUND_COLOR)
        self.options_menu.render(screen)

    def handle_click(self, mouse_click_position: tuple[float, float]) -> State:
        state = self.options_menu.handle_click(mouse_click_position)
        return state if state is not None else self

    def handle_quit(self) -> None:
        return
