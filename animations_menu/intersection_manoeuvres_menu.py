from animations_menu.options_menu import OptionToChoose, OptionsMenu
from constants import BACKGROUND_COLOR
from intersection.go_straight import IntersectionGoStraightAnimation
from intersection.turn_left import IntersectionTurnLeftAnimation
from intersection.turn_right import IntersectionTurnRightAnimation
from state import State

TITLE = "Choose Intersection Manoeuvre"
OPTIONS_COLUMNS_NUMBER = 3


class IntersectionManoeuvresMenu(State):
    def __init__(self, previous_state: State):
        super().__init__(previous_state=previous_state)
        self.options_menu = OptionsMenu(TITLE, OPTIONS_COLUMNS_NUMBER)
        self._add_option_to_choose(
            OptionToChoose(
                "Turn Left",
                "animationsScreenshots/screenshot12.png",
                IntersectionTurnLeftAnimation(self, True),
            )
        )
        self._add_option_to_choose(
            OptionToChoose(
                "Turn Right",
                "animationsScreenshots/screenshot12.png",
                IntersectionTurnRightAnimation(self, True),
            )
        )
        self._add_option_to_choose(
            OptionToChoose(
                "Go Straight",
                "animationsScreenshots/screenshot12.png",
                IntersectionGoStraightAnimation(self, True),
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
