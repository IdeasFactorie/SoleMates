# Shmup game
# Frozen Jam by tgfcoder <https://twitter.com/tgfcoder> licensed under CC-BY-3
# Art from Kenney.nl
# Tutorial by YouTube: KidsCanCode
import pygame
import random
from os import path

img_dir = path.join(path.dirname(__file__), 'img')
snd_dir = path.join(path.dirname(__file__), 'snd')

WIDTH = 1024
HEIGHT = 768
FPS = 60
POWERUP_TIME = 5000

# define colours
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

BAR_LENGTH = 100
BAR_HEIGHT = 10

# initialize pygame and create window
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("SOLEMATES BONUS")
clock = pygame.time.Clock()

font_name = pygame.font.match_font('helsinki')


class Player(pygame.sprite.Sprite):
    def __init__(self, player_img, bonus_level):
        pygame.sprite.Sprite.__init__(self)
        self.bonus_level = bonus_level
        self.image = pygame.transform.scale(player_img, (19, 59))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = 20
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = 100
        self.speedx = 0
        self.shield = 100
        self.shoot_delay = 250
        self.last_shot = pygame.time.get_ticks()
        self.lives = 3
        self.hidden = False
        self.hide_timer = pygame.time.get_ticks()
        self.power = 1
        self.power_time = pygame.time.get_ticks()

    def update(self):
        # timeout for powerups
        if self.power >= 2 and pygame.time.get_ticks() - self.power_time > POWERUP_TIME:
            self.power -= 1
            self.power_time = pygame.time.get_ticks()

        # unhide if hidden
        if self.hidden and pygame.time.get_ticks() - self.hide_timer > 1000:
            self.hidden = False
            self.rect.centerx = WIDTH / 2
            self.rect.bottom = 100

        self.speedx = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speedx = -8
        if keystate[pygame.K_RIGHT]:
            self.speedx = 8
        if keystate[pygame.K_SPACE]:
            self.shoot()
        self.rect.x += self.speedx
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0

    def powerup(self):
        self.power += 1
        self.power_time = pygame.time.get_ticks()

    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            if self.power == 1:
                bullet = Bullet(self.rect.centerx, self.rect.bottom, self.bonus_level.bullet_img)
                self.bonus_level.all_sprites.add(bullet)
                self.bonus_level.bullets.add(bullet)
                self.bonus_level.shoot_sound.play()
            if self.power >= 2:
                bullet1 = Bullet(self.rect.right, self.rect.centery, self.bonus_level.bullet_img)
                bullet2 = Bullet(self.rect.left, self.rect.centery, self.bonus_level.bullet_img)
                self.bonus_level.all_sprites.add(bullet1)
                self.bonus_level.all_sprites.add(bullet2)
                self.bonus_level.bullets.add(bullet1)
                self.bonus_level.bullets.add(bullet2)
                self.bonus_level.shoot_sound.play()

    def hide(self):
        # hide the player temporarily
        self.hidden = True
        self.hide_timer = pygame.time.get_ticks()
        self.rect.center = (WIDTH / 2, HEIGHT + 200)


class Mob(pygame.sprite.Sprite):
    def __init__(self, mob_img):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(mob_img, (57, 54))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * .85 / 2)
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.bottom = 822
        self.speedy = random.randrange(-8, -1)
        self.speedx = random.randrange(-3, 3)
        self.last_update = pygame.time.get_ticks()

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.top <= 0 or self.rect.left < -100 or self.rect.right > WIDTH + 100:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(822)
            self.speedy = random.randrange(-8, -1)


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, bullet_img):
        pygame.sprite.Sprite.__init__(self)
        self.image = bullet_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.top = y
        self.rect.centerx = x
        self.speedy = 10

    def update(self):
        self.rect.y += self.speedy
        # kill if it moves off the top of the screen
        if self.rect.bottom < 0:
            self.kill()


class Pow(pygame.sprite.Sprite):
    def __init__(self, center, powerup_images):
        pygame.sprite.Sprite.__init__(self)
        self.type = random.choice(['shield', 'gun'])
        self.image = powerup_images[self.type]
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.speedy = 5

    def update(self):
        self.rect.y += self.speedy
        # kill if it moves off the top of the screen
        if self.rect.top > HEIGHT:
            self.kill()


class Explosion(pygame.sprite.Sprite):
    def __init__(self, center, size, explosion_anim):

        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.explosion_anim = explosion_anim
        self.image = self.explosion_anim[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 75

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(self.explosion_anim[self.size]):
                self.kill()
            else:
                center = self.rect.center
                self.image = self.explosion_anim[self.size][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center


class BonusLevel:
    def __init__(self):
        # init variables
        self.all_sprites = pygame.sprite.Group()
        self.mobs = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.powerups = pygame.sprite.Group()

        # Load all game graphics
        self.background = pygame.image.load(path.join(img_dir, "background.png")).convert()
        self.background_rect = self.background.get_rect()
        self.player_img = pygame.image.load(path.join(img_dir, "socky.png")).convert_alpha()
        self.player_mini_img = pygame.image.load(path.join(img_dir, "lives.png")).convert_alpha()
        self.mob_img = pygame.image.load(path.join(img_dir, "spider.png")).convert_alpha()
        self.bullet_img = pygame.image.load(path.join(img_dir, "fluffball.png")).convert_alpha()
        self.explosion_anim = {'lg': [], 'sm': [], 'player': []}

        for i in range(9):
            filename = 'regularExplosion0{}.png'.format(i)
            img = pygame.image.load(path.join(img_dir, filename)).convert()
            img.set_colorkey(BLACK)
            img_lg = pygame.transform.scale(img, (75, 75))
            self.explosion_anim['lg'].append(img_lg)
            img_sm = pygame.transform.scale(img, (32, 32))
            self.explosion_anim['sm'].append(img_sm)
            filename = 'sonicExplosion0{}.png'.format(i)
            img = pygame.image.load(path.join(img_dir, filename)).convert()
            img.set_colorkey(BLACK)
            self.explosion_anim['player'].append(img)
        self.powerup_images = {'shield': pygame.image.load(path.join(img_dir, 'shield_gold.png')).convert(),
                               'gun': pygame.image.load(path.join(img_dir, 'bolt_gold.png')).convert()}

        # Load all game sounds
        self.shoot_sound = pygame.mixer.Sound(path.join(snd_dir, 'Laser_Shoot.wav'))
        self.shield_sound = pygame.mixer.Sound(path.join(snd_dir, 'pow4.wav'))
        self.power_sound = pygame.mixer.Sound(path.join(snd_dir, 'pow5.wav'))
        self.mob_death_sound = pygame.mixer.Sound(path.join(snd_dir, 'sdeath.wav'))
        self.player_die_sound = pygame.mixer.Sound(path.join(snd_dir, 'rumble1.ogg'))
        #pygame.mixer.music.load(path.join(snd_dir, 'tgfcoder-FrozenJam-SeamlessLoop.ogg'))
        pygame.mixer.music.set_volume(0.4)

#        pygame.mixer.music.play(loops=-1)

    @staticmethod
    def draw_text(surf, text, size, x, y):
        font = pygame.font.Font(font_name, size)
        text_surface = font.render(text, True, WHITE)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        surf.blit(text_surface, text_rect)

    def newmob(self):
        m = Mob(self.mob_img)
        self.all_sprites.add(m)
        self.mobs.add(m)

    @staticmethod
    def draw_shield_bar(surf, x, y, pct):
        if pct < 0:
            pct = 0

        fill = (pct / 100) * BAR_LENGTH
        outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
        fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
        pygame.draw.rect(surf, GREEN, fill_rect)
        pygame.draw.rect(surf, WHITE, outline_rect, 2)

    @staticmethod
    def draw_lives(surf, x, y, lives, img):
        for i in range(lives):
            img_rect = img.get_rect()
            img_rect.x = x + 30 * i
            img_rect.y = y
            surf.blit(img, img_rect)

    def show_go_screen(self):
        screen.blit(self.background, self.background_rect)
        self.draw_text(screen, "BONUS LEVEL!", 64, WIDTH / 2, HEIGHT / 4)
        self.draw_text(screen, "Arrow keys move, Space to fire", 22, WIDTH / 2, HEIGHT / 2)
        self.draw_text(screen, "Press a key to begin", 18, WIDTH / 2, HEIGHT * 3 / 4)
        pygame.display.flip()
        waiting = True
        while waiting:
            clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.KEYUP:
                    waiting = False

    def run(self):
        death_explosion = None
        score = None

        # Game loop
        game_over = True
        running = True
        while running:
            if game_over:
                self.show_go_screen()
                game_over = False
                player = Player(self.player_img, self)
                self.all_sprites.add(player)
                for i in range(8):
                    self.newmob()

                score = 0
            # keep loop running at the right speed
            clock.tick(FPS)
            # Process input (events)
            for event in pygame.event.get():
                # check for closing the window
                if event.type == pygame.QUIT:
                    running = False

            # Update
            self.all_sprites.update()

            # check to see if a bullet hit a mob
            hits = pygame.sprite.groupcollide(self.mobs, self.bullets, True, True)
            for hit in hits:
                score += 50 - hit.radius
                self.mob_death_sound.play()
                expl = Explosion(hit.rect.center, 'lg', self.explosion_anim)
                self.all_sprites.add(expl)
                if random.random() > 0.9:
                    power_up = Pow(hit.rect.center, self.powerup_images)
                    self.all_sprites.add(power_up)
                    self.powerups.add(power_up)
                self.newmob()

            # check to see if a mob hit the player
            hits = pygame.sprite.spritecollide(player, self.mobs, True, pygame.sprite.collide_circle)
            for hit in hits:
                player.shield -= hit.radius * 2
                expl = Explosion(hit.rect.center, 'sm', self.explosion_anim)
                self.all_sprites.add(expl)
                self.newmob()
                if player.shield <= 0:
                    self.player_die_sound.play()
                    death_explosion = Explosion(player.rect.center, 'player', self.explosion_anim)
                    self.all_sprites.add(death_explosion)
                    player.hide()
                    player.lives -= 1
                    player.shield = 100

            # check to see if player hit a powerup
            hits = pygame.sprite.spritecollide(player, self.powerups, True)
            for hit in hits:
                if hit.type == 'shield':
                    player.shield += random.randrange(10, 30)
                    self.shield_sound.play()
                    if player.shield >= 100:
                        player.shield = 100
                if hit.type == 'gun':
                    player.powerup()
                    self.power_sound.play()

            # if the player has died and the explosion has finished playing
            if player.lives == 0 and not death_explosion.alive():
                game_over = True

            # Draw / render
            screen.fill(BLACK)
            screen.blit(self.background, self.background_rect)
            self.all_sprites.draw(screen)
            self.draw_text(screen, str(score), 18, WIDTH / 2, 10)
            self.draw_shield_bar(screen, 5, 5, player.shield)
            self.draw_lives(screen, WIDTH - 100, 5, player.lives, self.player_mini_img)
            # *after* drawing everything, flip the display
            pygame.display.flip()
