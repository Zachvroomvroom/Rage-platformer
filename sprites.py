# Sprite classes for platform game
import pygame as pg
import random as rn
from settings import *
vec = pg.math.Vector2

class Player(pg.sprite.Sprite):
    def __init__(self, game):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.width = 40
        self.height = 40
        self.idle_img = []
        self.run_img_r = []
        self.run_img_l = []
        self.load_images()
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
        self.current_frame=0

        self.coyotetime = 5000
        now = pg.time.get_ticks()
        self.last_update = now

    def jump(self):
        print("Jump")
        # now = pg.time.get_ticks()
        # if now - self.coyotetime >= 5000:
        #     now = self.coyotetime
        #     print("no jump")
        # jump only if standing on a platform
        self.rect.x += 1
        hits = pg.sprite.spritecollide(self, self.game.platforms, False)
        if hits:
            self.jumps_used =0
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
        now = pg.time.get_ticks()
        if int(self.vel.x) != 0:
            self.running = True
        else:
            self.running = False
        if 0.05 >= int(self.vel.y) >= -0.05:
            self.jumping = True
        else:
            self.jumping = False
        if not self.running and not self.jumping:
            if now - self.last_update > 125:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.idle_img)
                self.image = self.idle_img[self.current_frame]
                self.rect = self.image.get_rect()
        if self.jumping:
            self.image = pg.image.load("P_sprites/bunny3.png")
            self.image = pg.transform.scale(self.image, (self.width, self.height))
            self.rect = self.image.get_rect()
        if self.running:
            if now - self.last_update > 100:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.run_img_r)
                if self.vel.x > 0:
                    self.image = self.run_img_r[self.current_frame]
                else:
                    self.image = self.run_img_l[self.current_frame]
                self.rect = self.image.get_rect()

    def load_images(self):
        # self.idle1r = pg.image.load("P_Sprites/bunny1.png")
        # self.idle2r = pg.image.load("P_Sprites/bunny2")
        # self.move1r = pg.image.load("P_Sprites/bunny3")
        # self.move2r = pg.image.load("P_Sprites/bunny4")
        for i in range(1, 3):

            filename = "P_Sprites/bunny{}.png".format(i)

            img = pg.image.load(filename)
            img = pg.transform.scale(img, (self.width, self.height))
            self.idle_img.append(img)
            # img = pg.transform.flip(img,True,False)
            # self.run_img_l.append(img)

        for i in range(3, 5):

            filename = "P_Sprites/bunny{}.png".format(i)
            img = pg.image.load(filename)
            img = pg.transform.scale(img, (self.width, self.height))
            self.run_img_r.append(img)
            img = pg.transform.flip(img,True,False)
            self.run_img_l.append(img)



    def update(self):
        self.animate()
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

class Cloud(pg.sprite.Sprite):
    def __init__(self, game):
        self._layer = CLOUD_LAYER
        self.groups = game.all_sprites, game.clouds
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = rn.choice(self.game.cloud_images)
        self.image.set_colorkey(BLACK)
        # self.image = pg.Surface((w, h))
        # self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        scale = rn.randrange(50, 101) / 100
        self.image = pg.transform.scale(self.image, (int(self.rect.width * scale), int(self.rect.height * scale)))
        self.rect.x = rn.randrange(WIDTH + self.rect.width)+500
        self.rect.y = rn.randrange(0,100)

    def update(self):
        if self.rect.right < 0:
            print('cloud')
            self.kill()

    # def load_images(self):
    #     for i in range(1,4):
    #         filename = "P_Sprites\idle{}.png".format(i)
    #         img = pg.image.load(filename)
    #         self.idle_img.append(img)

class Platform(pg.sprite.Sprite):
    def __init__(self, x, y, w, h,game):
        self.groups = game.all_sprites,game.platforms
        pg.sprite.Sprite.__init__(self,self.groups)
        self.game = game
        self.image = pg.Surface((w, h))
        self.image = pg.image.load("normal grass.png")
        self.image = pg.transform.scale(self.image, (w, h))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        if rn.randrange(100)<STAR_SPAWN_PCT:
            Star(self.game,self)

class Star(pg.sprite.Sprite):
    def __init__(self, game, plat):
        self.groups = game.all_sprites, game.stars
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.plat = plat
        self.type = rn.choice(['boost'])
        self.image = pg.image.load("Star.PNG")
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = self.plat.rect.centerx
        self.rect.bottom = self.plat.rect.top - 5

    def update(self):
        self.rect.bottom = self.plat.rect.top - 5
        if not self.game.platforms.has(self.plat):
            self.kill()