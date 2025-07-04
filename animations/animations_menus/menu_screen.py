import pygame
from animations.animations_menus.constants import (
    BACKGROUND_IMAGE_FILE_NAME,
    FONT_COLOR,
    FONT_FILENAME,
    TITLE_BACKGROUND_BORDER_RADIUS,
    TITLE_BACKGROUND_COLOR,
    TITLE_BACKGROUND_MARGIN,
    TITLE_BACKGROUND_TRANSPARENCY,
    TITLE_FONT_SIZE,
    TITLE_TOP_OFFSET,
)
from animations.animations_menus.options_panel.menu_options_panel import (
    MenuOptionsPanel,
)
from animations.previous_screen_button import PreviousScreenButton
from application_screen import ApplicationScreen
from constants import SCREEN_HEIGHT, SCREEN_WIDTH
from geometry.shapes.rectangle import AxisAlignedRectangle
from geometry.vector import Point
from utils import blit_surface, load_font, load_image


class MenuScreen(ApplicationScreen):
    def __init__(
        self,
        title: str,
        options_panel: MenuOptionsPanel,
        *,
        previous_app_screen: ApplicationScreen | None = None,
    ) -> None:
        self.previous_screen_button = (
            PreviousScreenButton(previous_app_screen) if previous_app_screen else None
        )
        self.background_image = pygame.transform.scale(
            load_image(BACKGROUND_IMAGE_FILE_NAME),
            (SCREEN_WIDTH, SCREEN_HEIGHT),
        )
        self.title_surface = load_font(FONT_FILENAME, TITLE_FONT_SIZE).render(
            title, True, FONT_COLOR
        )
        title_width = self.title_surface.get_width()
        self.title_top_left = Point(
            (SCREEN_WIDTH - title_width) // 2,
            SCREEN_HEIGHT - TITLE_TOP_OFFSET,
        )
        self.title_background_top_left = Point(
            (SCREEN_WIDTH - title_width) // 2 - TITLE_BACKGROUND_MARGIN,
            SCREEN_HEIGHT,
        )
        self.title_background_width = title_width + 2 * TITLE_BACKGROUND_MARGIN
        self.title_background_height = (
            TITLE_TOP_OFFSET + self.title_surface.get_height() + TITLE_BACKGROUND_MARGIN
        )
        self.options_panel = options_panel
        self.title_background = AxisAlignedRectangle(
            Point(SCREEN_WIDTH // 2, SCREEN_HEIGHT),
            self.title_background_width,
            self.title_background_height,
            TITLE_BACKGROUND_COLOR,
            border_rear_left_radius=TITLE_BACKGROUND_BORDER_RADIUS,
            border_rear_right_radius=TITLE_BACKGROUND_BORDER_RADIUS,
            transparency=TITLE_BACKGROUND_TRANSPARENCY,
        )

    def render_title(self, screen: pygame.Surface) -> None:
        self.title_background.draw(screen)
        blit_surface(screen, self.title_surface, self.title_top_left)

    def render_frame(self, screen: pygame.Surface) -> None:
        blit_surface(screen, self.background_image, Point(0, SCREEN_HEIGHT))
        self.render_title(screen)
        self.options_panel.render(screen)
        if self.previous_screen_button:
            self.previous_screen_button.render(screen)

    def handle_click(self, mouse_click_point: Point) -> ApplicationScreen:
        if self.previous_screen_button:
            previous_screen_requested = self.previous_screen_button.handle_click(
                mouse_click_point
            )
            if previous_screen_requested:
                return previous_screen_requested
        new_screen_to_generate = self.options_panel.handle_click(mouse_click_point)
        return new_screen_to_generate or self
