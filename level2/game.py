import pygame
import sys
import os
from os import path
from settings import *
from sprites import *
from tilemap import *
from hud import *
from player import *
from items import *


class Game:
    def __init__(self, screen, clock):
        self.screen = screen
        self.clock = clock
        self.load_data()

    def load_data(self):
        game_folder = path.dirname(__file__)
        img_folder = path.join(game_folder, '..', 'img')
        map_folder = game_folder
        # map files
        self.map = TiledMap(path.join(map_folder, 'level2.tmx'))
        self.map_img = self.map.make_map()
        self.map_rect = self.map_img.get_rect()

        # spritesheets
        self.player_spritesheet = Spritesheet(path.join(img_folder, PLAYER_SPRITESHEET))

        # enemy files
        self.spider_img = pygame.image.load(path.join(img_folder, SPIDER_IMG)).convert_alpha()
        self.vacuum_img = pygame.image.load(path.join(img_folder, VACUUM_IMG)).convert_alpha()


    # to start new game creates new instances of sprites, camera, tiles
    def new(self):
        self.all_sprites = pygame.sprite.Group()
        self.obstacles = pygame.sprite.Group()
        self.mobs = pygame.sprite.Group()
        self.hits = pygame.sprite.Group()
        self.socks = pygame.sprite.Group()
        self.items = pygame.sprite.Group()

        # fetches collision object data from tmx file
        for tile_object in self.map.tmxdata.objects:
            if tile_object.name == 'player':
                self.player = Player(self, tile_object.x, tile_object.y)
                # obj_center = vec(tile_object.x + tile_object.width / 2,
                #                  tile_object.y + tile_object.height / 2)
            if tile_object.name == 'obstacle':
                Obstacle(self, tile_object.x, tile_object.y,
                         tile_object.width, tile_object.height)
            if tile_object.name == 'boss':
                self.vacuum = Vacuum(self, tile_object.x, tile_object.y)
            if tile_object.name == 'mob':
                self.spider = Spider(self, tile_object.x, tile_object.y)
            if tile_object.name == 'clickable':
                Item(self, tile_object.x, tile_object.y)

        self.camera = Camera(self.map.width, self.map.height)


    # the gameloop
    def run(self):
        self.dt = self.clock.tick(FPS) / 1000
        self.events()
        self.update()
        self.draw()

    # to exit game
    def quit(self):
        pygame.quit()
        sys.exit()

    # updates all info per frame of game
    def update(self):
        self.all_sprites.update()
        self.camera.update(self.player)

        hits = pygame.sprite.groupcollide(self.socks, self.hits, False, True)
        for hit in hits:
            hit.health -= ZAP_DAMAGE
            if self.player.health < 0:
                self.player.lives -= 1
                self.player.health = 10
            if self.player.lives <= 0:
                self.show_go_screen()

    # renders everything to screen
    def draw(self):
        #pygame.display.set_caption("{:.2f}".format(self.clock.get_fps()))
        self.screen.blit(self.map_img, self.camera.apply_rect(self.map_rect))
        for sprite in self.all_sprites:
            if isinstance(sprite, Robot):
                sprite.draw_health()
            self.screen.blit(sprite.image, self.camera.apply(sprite))
        DrawHUD(self.player.health, self.player.lives, self.screen)
        pygame.display.flip()

    # keeps track of player input
    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.pos = pygame.mouse.get_pos()

    # for gameover
    def show_go_screen(self):
        pass
