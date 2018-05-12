from sprites import *

class Player(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.socks
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game

        self.walking = False
        self.current_frame = 0
        self.last_update = 0
        self.load_images()
        self.image = self.neutral_frames[0]

        self.rect = self.image.get_rect()
        self.radius = 15

        self.vel = vec(0, 0)
        self.pos = vec(x, y)

        self.health = PLAYER_HEALTH
        self.lives = PLAYER_LIVES

    def load_images(self):
        self.neutral_frames = [self.game.player_spritesheet.get_image(60, 0, 32, 32),
                               self.game.player_spritesheet.get_image(60, 33, 32, 31)]
        for frame in self.neutral_frames:
            frame.set_colorkey(BLACK)
        self.walk_frames_r = [self.game.player_spritesheet.get_image(0, 33, 59, 32),
                              self.game.player_spritesheet.get_image(0, 66, 59, 32),
                              self.game.player_spritesheet.get_image(0, 0, 59, 32),
                              self.game.player_spritesheet.get_image(0, 66, 59, 32)]
        for frame in self.walk_frames_r:
            frame.set_colorkey(BLACK)
        self.walk_frames_l = []
        for frame in self.walk_frames_r:
            self.walk_frames_l.append(pygame.transform.flip(frame, True, False))


    def get_keys(self):
        self.vel = vec(0, 0)
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT] or keystate[pygame.K_a]:
            self.vel.x = -PLAYER_SPEED
        if keystate[pygame.K_RIGHT] or keystate[pygame.K_d]:
            self.vel.x = PLAYER_SPEED
        if keystate[pygame.K_UP] or keystate[pygame.K_w]:
            self.vel.y = -PLAYER_SPEED
        if keystate[pygame.K_DOWN] or keystate[pygame.K_s]:
            self.vel.y = PLAYER_SPEED
        if self.vel.x != 0 and self.vel.y != 0:
            self.vel *= 0.7071

    def collide_with_obstacles(self, dir):
        movingLeft = self.vel.x > 0
        movingRight = self.vel.x < 0
        movingUp = self.vel.y > 0
        movingDown = self.vel.y < 0
        if dir == DIR_HORIZ:
            hits = pygame.sprite.spritecollide(self, self.game.obstacles, False)
            if hits:
                if movingLeft:
                    self.pos.x = hits[0].rect.left - self.rect.width
                if movingRight:
                    self.pos.x = hits[0].rect.right
                self.vel.x = 0
                self.rect.x = self.pos.x
        if dir == DIR_VERT:
            hits = pygame.sprite.spritecollide(self, self.game.obstacles, False)
            if hits:
                if movingUp:
                    self.pos.y = hits[0].rect.top - self.rect.height
                if movingDown:
                    self.pos.y = hits[0].rect.bottom
                self.vel.y = 0
                self.rect.y = self.pos.y


    def update(self):
        self.get_keys()
        self.animate()
        self.pos += self.vel * self.game.dt
        self.rect.x = self.pos.x
        self.collide_with_obstacles(DIR_HORIZ)
        self.rect.y = self.pos.y
        self.collide_with_obstacles(DIR_VERT)


    def animate(self):
        now = pygame.time.get_ticks()
        if self.vel.x != 0:
            self.walking = True
        else:
            self.walking = False

        if self.walking:
            if now - self.last_update > 200:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.walk_frames_l)
                bottom = self.rect.bottom
                if self.vel.x > 0:
                    self.image = self.walk_frames_r[self.current_frame]
                else:
                    self.image = self.walk_frames_l[self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom

        if not self.walking:
            if now - self.last_update > 600:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.neutral_frames)
                bottom = self.rect.bottom
                self.image = self.neutral_frames[self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom
