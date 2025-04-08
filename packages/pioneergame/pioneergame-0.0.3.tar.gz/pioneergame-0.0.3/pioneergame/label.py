import pygame as pg
from .rect import Rect
from .window import Window


class Label:
    def __init__(self, window: Window, x, y, color: str | pg.Color | tuple[int, int, int],
                 text: str = 'Sample Text', size: int = 25, font: str = "Courier", italic: bool = False):
        self.window = window
        self.x = x
        self.y = y
        self.color = color
        self.text = text
        self.font = pg.font.SysFont(font, size, False, italic)
        self._text_surface = self.font.render(self.text, True, self.color)

    def set_text(self, new_text: str | int | float) -> None:
        self.text = str(new_text)
        self._text_surface = self.font.render(self.text, True, self.color)

    def draw(self) -> None:
        self.window.screen.blit(self._text_surface, (self.x, self.y))

    def draw_box(self) -> None:
        pg.draw.rect(self.window.screen, (255, 0, 255), self.get_rect(), 1)

    @property
    def width(self) -> int: return self._text_surface.get_width()

    @property
    def height(self) -> int: return self._text_surface.get_height()

    @property
    def right(self) -> int: return self.x + self._text_surface.get_rect().right

    @property
    def left(self) -> int: return self.x + self._text_surface.get_rect().left

    @property
    def top(self) -> int: return self.y + self._text_surface.get_rect().top

    @property
    def bottom(self) -> int: return self.y + self._text_surface.get_rect().bottom

    def get_rect(self) -> Rect:  # TODO: change tuple to Rect analog
        return Rect(self.window, self.x, self.y, self.width, self.height)
