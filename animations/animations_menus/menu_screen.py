import pygame
from animations.animations_menus.constants import (
    FONT_COLOR,
    FONT_NAME,
    MENU_TITLE_FONT_SIZE,
    MENU_TITLE_TOP_OFFSET,
)
from animations.animations_menus.menu_options_panel import MenuOptionsPanel
from animations.previous_screen_button import PreviousScreenButton
from application_screen import ApplicationScreen
from constants import BACKGROUND_COLOR, SCREEN_HEIGHT, SCREEN_WIDTH
from drafter.drafter_base import DrafterBase
from geometry import Point


class MenuScreen(ApplicationScreen):
    def __init__(
        self,
        title: str,
        options_panel: MenuOptionsPanel,
        *,
        previous_app_screen: ApplicationScreen | None = None,
        background_image_path: str
        | None = "animations/animations_menus/screenshots/background.jpg",
        title_top_offset: int = MENU_TITLE_TOP_OFFSET,
    ) -> None:
        self.previous_screen_button = (
            PreviousScreenButton(previous_app_screen) if previous_app_screen else None
        )
        self.background_image = (
            pygame.transform.scale(
                pygame.image.load(background_image_path),
                (SCREEN_WIDTH, SCREEN_HEIGHT),
            )
            if background_image_path
            else None
        )
        pygame.font.init()
        self.title_font = pygame.font.SysFont(FONT_NAME, MENU_TITLE_FONT_SIZE)
        self.title_top_offset = title_top_offset
        self.title = title
        self.options_panel = options_panel

    def render_title(self, screen: pygame.Surface) -> None:
        title_surface = self.title_font.render(self.title, True, FONT_COLOR)
        title_rect = title_surface.get_rect(
            center=(screen.get_width() // 2, self.title_top_offset)
        )
        side_margin = 20
        DrafterBase().draw_basic_rectangle(
            screen,
            "white",
            Point((SCREEN_WIDTH - title_rect.width) / 2 - side_margin, SCREEN_HEIGHT),
            title_rect.width + 2 * side_margin,
            2 * title_rect.height,
            border_rear_left_radius=20,
            border_rear_right_radius=20,
            transparency=164,
        )
        screen.blit(title_surface, title_rect)

    def render_background(self, screen: pygame.Surface) -> None:
        if self.background_image:
            screen.blit(self.background_image, (0, 0))
        else:
            screen.fill(BACKGROUND_COLOR)

    def render_frame(self, screen: pygame.Surface) -> None:
        self.render_background(screen)
        self.render_title(screen)
        self.options_panel.render(screen)
        if self.previous_screen_button:
            self.previous_screen_button.render(screen)

    def handle_click(self, mouse_click_point: Point) -> ApplicationScreen | None:
        if self.previous_screen_button:
            previous_screen_requested = self.previous_screen_button.handle_click(
                mouse_click_point
            )
            if previous_screen_requested:
                return previous_screen_requested
        return self.options_panel.handle_click(mouse_click_point)
