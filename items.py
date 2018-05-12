import pygame
vec = pygame.math.Vector2

class Item(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self.pos = vec(x, y)
        self.rect = (x, y, 64, 64)
