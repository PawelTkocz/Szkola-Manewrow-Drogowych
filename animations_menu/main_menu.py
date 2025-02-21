from constants import BACKGROUND_COLOR
from options_menu import OptionsMenu, OptionToChoose
from state import State
from animations.intersection.go_straight import IntersectionGoStraight
from animations_menu.intersection_manoeuvres_menu import (
    IntersectionManoeuvresMenu,
)
from animations.intersection.turn_left import IntersectionTurnLeft
from animations.intersection.turn_right import IntersectionTurnRight

TITLE = "Choose Animation"
OPTIONS_COLUMNS_NUMBER = 3


class MainMenu(State):
    def __init__(self):
        super().__init__()
        self.options_menu = OptionsMenu(TITLE, OPTIONS_COLUMNS_NUMBER)
        self._add_option_to_choose(
            OptionToChoose(
                "Intersection",
                "animationsScreenshots/screenshot12.png",
                IntersectionManoeuvresMenu(self),
            )
        )
        self._add_option_to_choose(
            OptionToChoose(
                "Animation 2",
                "animationsScreenshots/screenshot12.png",
                IntersectionTurnRight(self),
            )
        )
        self._add_option_to_choose(
            OptionToChoose(
                "Animation 3",
                "animationsScreenshots/screenshot12.png",
                IntersectionGoStraight(self),
            )
        )
        self._add_option_to_choose(
            OptionToChoose(
                "Animation 4",
                "animationsScreenshots/screenshot12.png",
                IntersectionTurnLeft(self),
            )
        )
        self._add_option_to_choose(
            OptionToChoose(
                "Animation 5",
                "animationsScreenshots/screenshot12.png",
                IntersectionTurnLeft(self),
            )
        )
        self._add_option_to_choose(
            OptionToChoose(
                "Animation 6",
                "animationsScreenshots/screenshot12.png",
                IntersectionTurnLeft(self),
            )
        )

    def render_frame(self, screen):
        screen.fill(BACKGROUND_COLOR)
        self.options_menu.render(screen)

    def handle_click(self, mouse_click_position) -> State:
        state = self.options_menu.handle_click(mouse_click_position)
        return state if state is not None else self

    def handle_quit(self):
        return

    def _add_option_to_choose(self, option_to_choose: OptionToChoose):
        self.options_menu.add_option_to_choose(option_to_choose)
