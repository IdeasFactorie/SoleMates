import pygame

def health_bars(player_health):

    if player_health > 75:
        player_health_color = green
    elif player_health > 50:
        play_health_color = yellow
    else:
        player_health_color = red
    pygame.draw.rect(gameDisplay, player_health_color, (680, 25, player_health, 25))