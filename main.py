import pygame
import sys
import os
from os import path
from settings import *
from sprites import *
from tilemap import *
from player import *
from hud import *


class Game:
    def __init__(self):
        os.environ['SDL_VIDEO_CENTERED'] = '1'      # aligns game screen on computer screen
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.currentlevel = 1  # change to test different levels
        self.load_data()


    # level two
    def load_data(self):
        game_folder = path.dirname(__file__)
        img_folder = path.join(game_folder, 'img')
        map_folder = path.join(game_folder, 'map')

        #map files
        self.map = TiledMap(path.join(map_folder, 'level' + str(self.currentlevel) + '.tmx'))
        self.map_img = self.map.make_map()
        self.map_rect = self.map_img.get_rect()

        #player
        self.player_spritesheet = Spritesheet(path.join(img_folder, PLAYER_SPRITESHEET))

        #enemies
        self.clothes_spritesheet = Spritesheet(path.join(img_folder, CLOTHES_SPRITESHEET))
        self.robot_spritesheet = Spritesheet(path.join(img_folder, ROBOT_SPRITESHEET))
        self.spider_img = pygame.image.load(path.join(img_folder, SPIDER_IMG)).convert_alpha()
        self.vacuum_img = pygame.image.load(path.join(img_folder, VACUUM_IMG)).convert_alpha()
        self.item_images = {}
        for item in ITEM_IMAGES:
            self.item_images[item] = pygame.image.load(path.join(img_folder, ITEM_IMAGES[item])).convert_alpha()

        #items
        self.zap_img = pygame.image.load(path.join(img_folder, ZAP_IMG)).convert_alpha()

        #HUD
        self.inventory_img = pygame.image.load(path.join(img_folder, INVENTORY_IMG)).convert_alpha()
        self.zerolives_img = pygame.image.load(path.join(img_folder, ZERO_LIVES)).convert_alpha()
        self.onelives_img = pygame.image.load(path.join(img_folder, ONE_LIVES)).convert_alpha()
        self.twolives_img = pygame.image.load(path.join(img_folder, TWO_LIVES)).convert_alpha()
        self.threelives_img = pygame.image.load(path.join(img_folder, THREE_LIVES)).convert_alpha()
        self.fourlives_img = pygame.image.load(path.join(img_folder, FOUR_LIVES)).convert_alpha()

    # to start new game creates new instances of sprites, camera, tiles
    # level one
    def new(self):
        self.all_sprites = pygame.sprite.Group()
        self.obstacles = pygame.sprite.Group()
        self.mobs = pygame.sprite.Group()
        self.zaps = pygame.sprite.Group()
        self.socks = pygame.sprite.Group()
        self.items = pygame.sprite.Group()
 

        #fetches collision object data from tmx file
        for tile_object in self.map.tmxdata.objects:
            if tile_object.name == 'player':
                self.player = Player(self, tile_object.x, tile_object.y)
                obj_center = vec(tile_object.x + tile_object.width / 2,
                                 tile_object.y + tile_object.height / 2)
            if tile_object.name == 'obstacle':
                Obstacle(self, tile_object.x, tile_object.y,
                         tile_object.width, tile_object.height)
            if tile_object.name == 'player_obstacle':
                PlayerObstacle(self, tile_object.x, tile_object.y,
                         tile_object.width, tile_object.height)
            if tile_object.name == 'boss':
                if self.currentlevel == 1:
                    self.robot = Robot(self, tile_object.x, tile_object.y)
                if self.currentlevel == 2:
                    self.vacuum = Vacuum(self, tile_object.x, tile_object.y)
            if tile_object.name == 'mob':
                if self.currentlevel == 1:
                    self.clothes = Clothes(self, tile_object.x, tile_object.y)
                if self.currentlevel == 2:
                    self.spider = Spider(self, tile_object.x, tile_object.y)

        self.camera = Camera(self.map.width, self.map.height)

    # the gameloop
    def run(self):
        self.playing = True
        while self.playing:
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
        # bullets hit socky
        hits = pygame.sprite.groupcollide(self.socks, self.zaps, False, True)
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


    # for menu
    def show_start_screen(self):
        pass


    # for gameover
    def show_go_screen(self):
        pass


testgame = Game()
testgame.show_start_screen()
while True:
    testgame.new()
    testgame.run()

pygame.quit()