import pygame

from Constants import BACKGROUND_COLOR
from OptionToChoose import OptionToChoose
from OptionsMenu import OptionsMenu
from State import State
from animations.intersection.TurnLeftState import IntersectionTurnLeftState

TITLE = "Choose Animation"
OPTIONS_COLUMNS_NUMBER = 3


class MainMenu(State):
    def __init__(self):
        super().__init__()
        self.options_menu = OptionsMenu(TITLE, OPTIONS_COLUMNS_NUMBER)
        self._add_option_to_choose(
            OptionToChoose(
                "Animation 1",
                "animationsScreenshots/screenshot12.png",
                IntersectionTurnLeftState(self),
            )
        )

    def render_frame(self, screen):
        screen.fill(BACKGROUND_COLOR)
        self.options_menu.render(screen)

    def handle_click(self, mouse_click_position) -> State:
        state = self.options_menu.handle_click(mouse_click_position)
        return state if state is not None else self

    def _add_option_to_choose(self, option_to_choose: OptionToChoose):
        self.options_menu.add_option_to_choose(option_to_choose)
