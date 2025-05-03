import pygame


_screen: pygame.Surface | None = None


def init_screen(width: int, height: int) -> None:
    global _screen
    _screen = pygame.display.set_mode((width, height))


def get_screen() -> pygame.Surface:
    if _screen is None:
        raise ValueError("Screen must be initialized before access.")
    return _screen
