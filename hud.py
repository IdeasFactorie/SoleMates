import sys
import pygame
from settings import *


class HUD(pygame.sprite.Sprite):

    def __init__(self, surf, health, x, y, numlives):
        pygame.sprite.Sprite.__init__(self)
        self.surf = surf
        self.health = health
        self.numlives = numlives
        inventory = INVENTORY_IMG

        livesGraphic = FOUR_LIVES
        if numlives == 0:
            livesGraphic = ZERO_LIVES
        if numlives == 1:
            livesGraphic = ONE_LIVES
        if numlives == 2:
            livesGraphic = TWO_LIVES
        if numlives == 3:
            livesGraphic = THREE_LIVES
        if numlives == 4:
            livesGraphic = FOUR_LIVES



        if health < 0:
            health = 0
        fill = health * 10
        outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
        fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
        if health > 6:
            colour = GREEN
        elif health > 3:
            colour = YELLOW
        else:
            colour = RED

        pygame.draw.rect(surf, BLACK, outline_rect)
        pygame.draw.rect(surf, colour, fill_rect)
        #surf.blit(livesGraphic, (150, 15))
        #surf.blit(inventory, (785, 10))






