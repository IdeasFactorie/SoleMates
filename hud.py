import sys
import pygame
from settings import *
from os import path


class DrawHUD(pygame.sprite.Sprite):

    def __init__(self, health, numlives, surface):
        pygame.sprite.Sprite.__init__(self)
        self.health = health
        self.numlives = numlives
        self.surface = surface

        game_folder = path.dirname(__file__)
        img_folder = path.join(game_folder, 'img')

        self.inventory_img = pygame.image.load(path.join(img_folder, INVENTORY_IMG)).convert_alpha()
        self.zerolives_img = pygame.image.load(path.join(img_folder, ZERO_LIVES)).convert_alpha()
        self.onelives_img = pygame.image.load(path.join(img_folder, ONE_LIVES)).convert_alpha()
        self.twolives_img = pygame.image.load(path.join(img_folder, TWO_LIVES)).convert_alpha()
        self.threelives_img = pygame.image.load(path.join(img_folder, THREE_LIVES)).convert_alpha()
        self.fourlives_img = pygame.image.load(path.join(img_folder, FOUR_LIVES)).convert_alpha()
        self.healthborder_img = pygame.image.load(path.join(img_folder, HEALTH_BORDER)).convert_alpha()

        fill = self.health * 10
        self.outline_rect = pygame.Rect(13, 13, BAR_LENGTH, BAR_HEIGHT)
        self.fill_rect = pygame.Rect(13, 13, fill, BAR_HEIGHT)

        if self.health > 6:
            self.colour = GREEN
        elif self.health > 3:
            self.colour = YELLOW
        else:
            self.colour = RED

        if numlives == 0:
            livesgraphic = self.zerolives_img
        elif numlives == 1:
            livesgraphic = self.onelives_img
        elif numlives == 2:
            livesgraphic = self.twolives_img
        elif numlives == 3:
            livesgraphic = self.threelives_img
        else:
            livesgraphic = self.fourlives_img

        pygame.draw.rect(self.surface, self.colour, self.fill_rect)
        self.surface.blit(self.healthborder_img, (3, 3))
        self.surface.blit(livesgraphic, (140, 8))
        self.surface.blit(self.inventory_img, (790, 3))

