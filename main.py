import pygame
import sys
import os
from os import path
from settings import *
from sprites import *
from tilemap import *
from hud import *

#HUD functions
# def draw_player_health(surf, x, y, health):
#     if health < 0:
#         health = 0
#     fill = health * 10
#     outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
#     fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
#     if health > 6:
#         colour = GREEN
#     elif health > 3:
#         colour = YELLOW
#     else:
#         colour = RED
#
#     pygame.draw.rect(surf, BLACK, outline_rect)
#     pygame.draw.rect(surf, colour, fill_rect)

class Game:
    def __init__(self):
        os.environ['SDL_VIDEO_CENTERED'] = '1'      # aligns game screen on computer screen
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.load_data()


    # loads image assets and tile map co-ords
    # level one
    # def load_data(self):
    #     game_folder = path.dirname(__file__)
    #     img_folder = path.join(game_folder, 'img')
    #     map_folder = path.join(game_folder, 'map')
    #     self.map = TiledMap(path.join(map_folder, 'level1.tmx'))
    #     self.map_img = self.map.make_map()
    #     self.map_rect = self.map_img.get_rect()
    #
    #     self.player_img = pygame.image.load(path.join(img_folder, PLAYER_IMG)).convert_alpha()
    #     self.robot_img = pygame.image.load(path.join(img_folder, ROBOT_IMG)).convert_alpha()
    #     self.zap_img = pygame.image.load(path.join(img_folder, ZAP_IMG)).convert_alpha()
    #     self.clothes_img = pygame.image.load(path.join(img_folder, CLOTHES_IMG)).convert_alpha()

    # level two
    def load_data(self):
        game_folder = path.dirname(__file__)
        img_folder = path.join(game_folder, 'img')
        map_folder = path.join(game_folder, 'map')
        #map files
        self.map = TiledMap(path.join(map_folder, 'level1.tmx'))
        self.map_img = self.map.make_map()
        self.map_rect = self.map_img.get_rect()

        #spritesheets
        self.player_spritesheet = Spritesheet(path.join(img_folder, PLAYER_SPRITESHEET))
        self.clothes_spritesheet = Spritesheet(path.join(img_folder, CLOTHES_SPRITESHEET))
        self.robot_spritesheet = Spritesheet(path.join(img_folder, ROBOT_SPRITESHEET))

        #enemy files
        self.spider_img = pygame.image.load(path.join(img_folder, SPIDER_IMG)).convert_alpha()
        self.vacuum_img = pygame.image.load(path.join(img_folder, VACUUM_IMG)).convert_alpha()

        #item files
        self.zap_img = pygame.image.load(path.join(img_folder, ZAP_IMG)).convert_alpha()

        #HUD files
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

        #fetches collision object data from tmx file
        for tile_object in self.map.tmxdata.objects:
            if tile_object.name == 'player':
                self.player = Player(self, tile_object.x, tile_object.y)
            if tile_object.name == 'obstacle':
                Obstacle(self, tile_object.x, tile_object.y,
                         tile_object.width, tile_object.height)
            if tile_object.name == 'boss':
                self.robot = Robot(self, tile_object.x, tile_object.y)
            if tile_object.name == 'mob':
                self.clothes = Clothes(self, tile_object.x, tile_object.y)

        #Generates bullets
        self.camera = Camera(self.map.width, self.map.height)

    #level two
    # def new(self):
    #     self.all_sprites = pygame.sprite.Group()
    #     self.obstacles = pygame.sprite.Group()
    #     self.mobs = pygame.sprite.Group()
    #     self.zaps = pygame.sprite.Group
    #
    #     #fetches collision object data from tmx file
    #     for tile_object in self.map.tmxdata.objects:
    #         if tile_object.name == 'player':
    #             self.player = Player(self, tile_object.x, tile_object.y)
    #         if tile_object.name == 'wall':
    #             Obstacle(self, tile_object.x, tile_object.y,
    #                      tile_object.width, tile_object.height)
    #         if tile_object.name == 'furniture':
    #             Obstacle(self, tile_object.x, tile_object.y,
    #                      tile_object.width, tile_object.height)
    #         if tile_object.name == 'boss':
    #             self.vacuum = Vacuum(self, tile_object.x, tile_object.y)
    #         if tile_object.name == 'mob':
    #             self.spider = Spider(self, tile_object.x, tile_object.y)
    #     self.camera = Camera(self.map.width, self.map.height)


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

    # renders everything to screen
    def draw(self):
        pygame.display.set_caption("{:.2f}".format(self.clock.get_fps()))
        self.screen.blit(self.map_img, self.camera.apply_rect(self.map_rect))
        for sprite in self.all_sprites:
            if isinstance(sprite, Robot):
                sprite.draw_health()
            self.screen.blit(sprite.image, self.camera.apply(sprite))
        HUD(self.screen, self.player.health, 20, 20, self.player.lives)
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