from typing import TypedDict

from application_screen import ApplicationScreen


class OptionTileDescription(TypedDict):
    image_path: str
    on_click_app_screen: ApplicationScreen


class ListOptionDescription(TypedDict):
    text: str
    on_click_app_screen: ApplicationScreen
