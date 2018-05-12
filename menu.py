import pygame
from settings import *
from eventtypes import *


class MenuItem:
    def __init__(self, menu, label, activate_func, disabled=False):
        self.disabled = disabled
        self.label = label
        self._activate_func = activate_func
        self.normal_color = BLACK
        self.hover_color = RED
        self.scale = 1
        self.color = self.normal_color
        self.font = pygame.font.Font('helsinki.ttf', 60)

    def surface(self):
        return self.font.render(self.label, 1, self.color)

    def activate(self):
        pass

    def mouse_over(self):
        self.scale = 1.1
        self.color = self.hover_color

    def mouse_off(self):
        self.scale = 1
        self.color = self.normal_color


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
        self._cur_menu = "TOP_MENU"

        self._menus = {
            "TOP_MENU": self._render_items(self._top_menu()),
            "DIFFICULTY_MENU": self._render_items(self._difficulty_select_menu())
        }

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

    def _render_items(self, menu_items):
        items = []

        for index, menu_item in enumerate(menu_items):
            label_surface = menu_item.surface()
            (label_w, label_h) = label_surface.get_size()

            posx = (self._screen_width / 2) - (label_w / 2)
            total_height = len(self._label_strings) * label_h
            posy = (self._screen_height / 2 - total_height / 2) + (index * label_h)
            items.append([label_surface, (posx, posy), menu_item])

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

        for label_surface, (posx, posy), _ in self._menus[self._cur_menu]:
            self.screen.blit(label_surface, (posx, posy))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONUP:
            self.handle_mouse_click()
        if event.type == MENU_CLICK_EVENT:
            self.handle_menu_click(event.menu_item)

    def handle_menu_click(self, menu_item):
        if menu_item.label == "New Game":
            self._cur_menu = "DIFFICULTY_MENU"
        elif (menu_item.label == "Easy" or
              menu_item.label == "Hard" or
              menu_item.label == "Medium"):
            pygame.event.post(pygame.event.Event(START_LEVEL1_EVENT, dict()))

    def handle_mouse_click(self):
        (mouse_x, mouse_y) = pygame.mouse.get_pos()

        for label_surface, (posx, posy), menu_item in self._menus[self._cur_menu]:
            (label_w, label_h) = label_surface.get_size()
            label_rect = pygame.Rect(posx, posy, label_w, label_h)

            if label_rect.collidepoint(mouse_x, mouse_y):
                pygame.event.post(pygame.event.Event(MENU_CLICK_EVENT, menu_item=menu_item))


    def check_mouse(self):
        (mouse_x, mouse_y) = pygame.mouse.get_pos()

        for label_surface, (posx, posy), menu_item in self._menus[self._cur_menu]:
            (label_w, label_h) = label_surface.get_size()
            label_rect = pygame.Rect(posx, posy, label_w, label_h)

            if label_rect.collidepoint(mouse_x, mouse_y):
                menu_item.mouse_over()
                label_surface.blit(menu_item.surface(), (0, 0))
            else:
                menu_item.mouse_off()
                label_surface.blit(menu_item.surface(), (0, 0))


    def run(self):
        self.clock.tick(FPS)
        self.check_mouse()
        self._render()
        pygame.display.flip()
