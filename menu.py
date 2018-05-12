import pygame
from settings import *

class MenuItem:
    def __init__(self, menu, label, activate_func, disabled=False):
        self.disabled = disabled
        self.label = label
        self._menu = menu
        self._activate_func = activate_func

    def activate(self):
        self._activate_func(self._menu)


class Menu:
    def __init__(self,
                 screen,
                 clock,
                 bg_color=(252, 179, 53),
                 font='helsinki.ttf',
                 font_size=60,
                 font_color=(0, 0, 0),
                 disabled_color=(100, 100, 100)):

        self._screen_width, self._screen_height = (WIDTH, HEIGHT)
        self.screen = screen
        self.clock = clock
        self._disabled_color = disabled_color
        self._font_color = font_color
        self.bg_color = bg_color
        self.font_size = font_size
        self.font = pygame.font.Font(font, font_size)
        self._items = []
        self._label_strings = ["New Game", "Level Select", "Options", "Exit"]
        self._cur_menu = self._top_menu

        self._menus = {
            "TOP_MENU": self._get_items(self._top_menu),
            "DIFFICULTY_MENU": self._get_items(self._difficulty_select_menu)

        }

        self._top_menu_items = self._get_items(self._top_menu)
        self._difficulty_menu_items = self._get_items(self._difficulty_select_menu)

    def _new_game(self):
        pass

    def _level_select(self):
        pass

    def _options(self):
        pass

    def _exit(self):
        pass

    def _top_menu(self):
        return [
            MenuItem(self, "New Game", self._new_game),
            MenuItem(self, "Level Select", self._level_select),
            MenuItem(self, "Options", self._options),
            MenuItem(self, "Exit", self._exit)
        ]

    def _difficulty_select_menu(self):
        return [
            MenuItem(self, "Easy", self._set_easy_difficulty),
            MenuItem(self, "Medium", self._set_easy_difficulty),
            MenuItem(self, "Hard", self._set_easy_difficulty)
        ]

    def _get_items(self, menu_func):
        items = []

        for index, menu_item in enumerate(menu_func()):
            if menu_item.disabled:
                label_surface = self.font.render(menu_item.label, 1, self._disabled_color)
            else:
                label_surface = self.font.render(menu_item.label, 1, self._font_color)

            (_, _, label_w, label_h) = label_surface.get_rect()

            posx = (self._screen_width / 2) - (label_w / 2)
            total_height = len(self._label_strings) * label_h
            posy = (self._screen_height / 2 - total_height / 2) + (index * label_h)
            items.append([label_surface, (posx, posy)])

        return items

    def _handle_mouse_move(self):
        pass

    def _handle_mouse_click(self):
        pass

    def _render_header(self, screen):
        pass

    def _set_easy_difficulty(self):
        pass

    def _render(self):
        self.screen.fill(self.bg_color)

        for label_surface, (posx, posy) in self._get_items(self._cur_menu):
            self.screen.blit(label_surface, (posx, posy))

    def run(self):
        self.clock.tick(FPS)
        self._render()
        pygame.display.flip()
