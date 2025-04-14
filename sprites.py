# Sprite classes for platform game
import pygame as pg
from settings import *
vec = pg.math.Vector2

class Player(pg.sprite.Sprite):
    def __init__(self, game):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.idle_img = []
        self.image = pg.Surface((30, 40))
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)
        self.pos = vec(WIDTH / 2, HEIGHT / 2)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.track = 0
        self.far = 0
        self.stop = False
        self.count = 0

        self.dashes = 1
        self.dashes_used = 0
        self.jumps = 1
        self.jumps_used = 0

        self.animation = 'idle'

        self.coyotetime = 0

    def jump(self):
        now = pg.time.get_ticks()
        # jump only if standing on a platform
        self.rect.x += 1
        hits = pg.sprite.spritecollide(self, self.game.platforms, False)
        self.rect.x -= 1
        if self.jumps_used < self.jumps:
            self.vel.y = -20
            self.jumps_used += 1

    def dash(self):
        # dash only if dashes are left
        keys = pg.key.get_pressed()

        if self.dashes_used < self.dashes:
            if keys[pg.K_a]:
                self.vel.x = -30
                self.dashes_used += 1
            if keys[pg.K_d]:
                self.vel.x = 30
                self.dashes_used += 1

    def animate(self):
        pass

    def load_images(self):
        pass

    def update(self):
        self.acc = vec(0, PLAYER_GRAV)
        keys = pg.key.get_pressed()
        if keys[pg.K_a]:
            self.acc.x = -PLAYER_ACC
        if keys[pg.K_d]:
            self.acc.x = PLAYER_ACC
        now = pg.time.get_ticks()
        hits = pg.sprite.spritecollide(self, self.game.platforms, False)
        if hits:
            self.dashes_used = 0
            self.jumps_used = 0

        # apply friction
        self.acc.x += self.vel.x * PLAYER_FRICTION
        # equations of motion
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
        #NO WRAP OR OFF-SCREEN
        if self.pos.x > WIDTH:
            self.pos.x = WIDTH
        if self.pos.x < 0:
            self.pos.x = 0

        self.rect.midbottom = self.pos







































    # def load_images(self):
    #     for i in range(1,4):
    #         filename = "P_Sprites\idle{}.png".format(i)
    #         img = pg.image.load(filename)
    #         self.idle_img.append(img)

class Platform(pg.sprite.Sprite):
    def __init__(self, x, y, w, h):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((w, h))
        self.image.fill(GRASSGREEN)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y