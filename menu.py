# Reference tutorial: https://nebelprog.wordpress.com/2013/08/14/create-a-simple-game-menu-with-pygame-pt-1-writing-the-menu-options-to-the-screen/

import pygame

pygame.init()


class Menu():
    def __init__(self,
                 game,
                 screen_dim,
                 bg_color=(252, 179, 53),
                 font='helsinki.ttf',
                 font_size=60,
                 font_color=(0, 0, 0)):
        (_, _, self._screen_width, self._screen_height) = screen_dim

        self._font_color = font_color
        self.bg_color = bg_color
        self.font_size = font_size
        self.font = pygame.font.SysFont(font, font_size)
        self.font_color = font_color
        self._items = []
        self._label_strings = ["New Game", "Level Select", "Options", "Exit"]
        game.register_render_func(self._render)

    def _get_items(self):
        items = []

        for index, label_string in enumerate(self._label_strings):
            label_surface = self.font.render(label_string, 1, self._font_color)

            (_, _, label_w, label_h) = label_surface.get_rect()

            posx = (self._screen_width / 2) - (label_w / 2)
            total_height = len(self._label_strings) * label_h
            posy = (self._screen_height / 2 - total_height / 2) + (index * label_h)
            items.append([label_surface, (posx, posy)])

        return items

    def _render(self, screen):
        screen.fill(self.bg_color)

        for label_surface, (posx, posy) in self._get_items():
            screen.blit(label_surface, (posx, posy))
