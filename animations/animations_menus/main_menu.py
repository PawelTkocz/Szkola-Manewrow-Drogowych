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
    MAIN_MENU_OPTIONS_COLUMNS_NUMBER,
    MAIN_MENU_TITLE,
    MENU_OPTIONS_IMAGE_SIDE,
    MENU_OPTIONS_X_SPACING,
    MENU_OPTIONS_Y_SPACING,
    MENU_TITLE_TOP_OFFSET,
)
from animations.animations_menus.intersection_manoeuvres_menu import (
    IntersectionManoeuvresMenu,
)
from animations.animations_menus.options_menu import OptionsMenu
from constants import BACKGROUND_COLOR, SCREEN_HEIGHT, SCREEN_WIDTH
from state import State


class MainMenu(State):
    def __init__(self):
        super().__init__()
        self.options_menu = OptionsMenu(
            MAIN_MENU_TITLE,
            MAIN_MENU_OPTIONS_COLUMNS_NUMBER,
            SCREEN_HEIGHT,
            SCREEN_WIDTH,
            MENU_TITLE_TOP_OFFSET,
            MENU_OPTIONS_X_SPACING,
            MENU_OPTIONS_Y_SPACING,
            MENU_OPTIONS_IMAGE_SIDE,
        )
        # you can pass all option items in init as list
        self.options_menu.add_option_item(
            {
                "title": "Intersection",
                "image_path": "animationsScreenshots/screenshot12.png",
                "on_click_state": IntersectionManoeuvresMenu(self),
            }
        )
        self.options_menu.add_option_item(
            {
                "title": "Animation 2",
                "image_path": "animationsScreenshots/screenshot12.png",
                "on_click_state": IntersectionTurnRightAnimation(self),
            }
        )
        self.options_menu.add_option_item(
            {
                "title": "Animation 3",
                "image_path": "animationsScreenshots/screenshot12.png",
                "on_click_state": IntersectionGoStraightAnimation(self),
            }
        )
        self.options_menu.add_option_item(
            {
                "title": "Animation 4",
                "image_path": "animationsScreenshots/screenshot12.png",
                "on_click_state": IntersectionTurnLeftAnimation(self),
            }
        )
        self.options_menu.add_option_item(
            {
                "title": "Animation 5",
                "image_path": "animationsScreenshots/screenshot12.png",
                "on_click_state": IntersectionTurnLeftAnimation(self),
            }
        )
        self.options_menu.add_option_item(
            {
                "title": "Animation 6",
                "image_path": "animationsScreenshots/screenshot12.png",
                "on_click_state": IntersectionTurnLeftAnimation(self),
            }
        )

    def render_frame(self, screen: Surface):
        screen.fill(BACKGROUND_COLOR)
        self.options_menu.render(screen)

    def handle_click(self, mouse_click_position) -> State:
        state = self.options_menu.handle_click(mouse_click_position)
        return state if state is not None else self

    def handle_quit(self):
        return
