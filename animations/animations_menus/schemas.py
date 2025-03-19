from typing import TypedDict

from state import State


class OptionItemDescription(TypedDict):
    title: str
    image_path: str
    on_click_state: State
