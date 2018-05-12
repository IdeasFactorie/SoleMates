from menu import Menu
from bonus_level import BonusLevel
from level1 import Level1
import pygame
import os
import sys
from settings import *
from eventtypes import *

STATE_BONUS_LEVEL = "BONUS_LEVEL"
STATE_LEVEL1 = "LEVEL_1"
STATE_LEVEL2 = "LEVEL_2"
STATE_MENU = "MENU"

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(TITLE)
clock = pygame.time.Clock()
os.environ['SDL_VIDEO_CENTERED'] = '1'

menu = Menu(screen, clock)
bonus_level = BonusLevel()
level1 = Level1(screen, clock)

state = STATE_MENU

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == START_LEVEL1_EVENT:
            state = STATE_LEVEL1
            level1.new()
        elif event.type == START_LEVEL2_EVENT:
            pass
        elif event.type == START_BONUS_LEVEL_EVENT:
            state = STATE_BONUS_LEVEL
        else:
            if state == STATE_MENU:
                menu.handle_event(event)
            else:
                pass
    if state == STATE_MENU:
        menu.run()
    elif state == STATE_LEVEL1:
        level1.run()
    elif state == STATE_BONUS_LEVEL:
        bonus_level.run()
