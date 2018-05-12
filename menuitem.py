import pygame
from settings import *

pygame.init()


class MenuItem:
    def __init__(self, label, item_id, disabled=False):
        self.item_id = item_id
        self.disabled = disabled
        self.label = label
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
