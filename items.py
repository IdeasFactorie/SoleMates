import pygame
vec = pygame.math.Vector2

class Fluffball(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.collectables
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.fluffball_img
        self.rect = self.image.get_rect()
        self.pos = vec(x, y)

    def update(self):
        self.rect.y = self.pos.y
        self.rect.x = self.pos.x
        self.get_mouse()

    def get_mouse(self):
        mouse_pos = pygame.mouse.get_pos()
        mouse_sprite = pygame.sprite.Sprite
        mouse_sprite.rect = pygame.Rect(mouse_pos, (5, 5))
        item_detected = pygame.sprite.spritecollideany(mouse_sprite, self.game.collectables)
        #print(item_detected)






