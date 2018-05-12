from game import Game
from menu import Menu
import pygame
import os
import sys
from settings import *
from eventtypes import *

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(TITLE)
clock = pygame.time.Clock()
os.environ['SDL_VIDEO_CENTERED'] = '1'

game = Game(screen, clock)
menu = Menu(screen, clock)

state = "MENU"

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == START_LEVEL1_EVENT:
            state = "GAME"
            game.new()
        else:
            if state == "MENU":
                menu.handle_event(event)
            elif state == "GAME":
                pass
    if state == "MENU":
        menu.run()
    elif state == "GAME":
        game.run()
