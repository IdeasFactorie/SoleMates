from game import Game
from menu import Menu
import pygame
import os
import sys
from settings import *

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(TITLE)
clock = pygame.time.Clock()
os.environ['SDL_VIDEO_CENTERED'] = '1'

game = Game(screen, clock)
menu = Menu(screen, clock)


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        else:
            menu.handle_event(event)
    menu.run()


