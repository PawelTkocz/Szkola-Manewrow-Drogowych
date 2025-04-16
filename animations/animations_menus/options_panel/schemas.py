from typing import Callable, TypedDict

from application_screen import ApplicationScreen


class OptionTileDescription(TypedDict):
    image_file_name: str
    on_click_app_screen_generator: Callable[[], ApplicationScreen]


class ListOptionDescription(TypedDict):
    text: str
    on_click_app_screen_generator: Callable[[], ApplicationScreen]
