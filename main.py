import pygame as pg
import random
from settings import *
from sprites import *

class Game:
    def __init__(self):
        # initialize game window, etc
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.running = True

    def new(self):
        # start a new game
        self.all_sprites = pg.sprite.Group()
        self.platforms = pg.sprite.Group()
        self.player = Player(self)
        self.all_sprites.add(self.player)
        for plat in PLATFORM_LIST:
            p = Platform(*plat)
            self.all_sprites.add(p)
            self.platforms.add(p)
        self.run()

    def run(self):
        # Game Loop
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def update(self):
        # Game Loop - Update
        self.all_sprites.update()
        # check if player hits a platform - only if falling
        if self.player.vel.y > 0:
            hits = pg.sprite.spritecollide(self.player, self.platforms, False)
            if hits:
                self.player.pos.y = hits[0].rect.top
                self.player.vel.y = 0
        if self.player.rect.y > HEIGHT:
           self.new()
        # if player reaches to 1/4 of screen
        if self.player.vel.x > .05:
            self.player.track += 1
        if self.player.vel.x < -.05:
            self.player.track -= 1
        if self.player.track > self.player.far:
            self.player.far = self.player.track
        if self.player.stop :
            self.player.vel.x = 0
        if self.player.rect.right >= 3 * WIDTH / 5:
            if self.player.vel.x > .05:
                self.player.count += 1

            self.player.pos.x -= abs(self.player.vel.x)
            for plat in self.platforms:
                plat.rect.x -= abs(self.player.vel.x)
                if self.player.count > 50:
                    height = random.randrange(100, 251)
                    x = random.randrange(WIDTH + 50, WIDTH + 150)
                    width = x - WIDTH
                    #     y = random.randrange(-75,-30)
                    p = Platform(x, HEIGHT - height, width, height)
                    self.platforms.add(p)
                    self.all_sprites.add(p)
                    self.player.count = 0
        if self.player.vel.x < -.05:
            self.player.count -= 1
            if self.player.count < 0:
                self.player.count = 0
        if self.player.rect.left <= WIDTH / 2.5:
            self.player.pos.x += abs(self.player.vel.x)
            for plat in self.platforms:
                plat.rect.x += abs(self.player.vel.x)

    def events(self):
        # Game Loop - events
        for event in pg.event.get():
            # check for closing window
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    self.player.jump()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_w:
                    self.player.dash()

    def draw(self):
        # Game Loop - draw
        self.screen.fill(SKYBLUE)
        self.all_sprites.draw(self.screen)
        # *after* drawing everything, flip the display
        pg.display.flip()

    def show_start_screen(self):
        # game splash/start screen
        pass

    def show_go_screen(self):
        # game over/continue
        pass

g = Game()
g.show_start_screen()
while g.running:
    g.new()
    g.show_go_screen()

pg.quit()