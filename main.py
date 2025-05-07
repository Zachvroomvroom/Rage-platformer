import pygame as pg
import random as rn
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
        self.font_name = pg.font.match_font(FONT_NAME)

    def draw_text(self,surf,text,size,x,y,color):
        font = pg.font.Font(self.font_name, size)
        text_surface = font.render(text,True,color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x,y)
        surf.blit(text_surface,text_rect)

    def new(self):
        # start a new game
        self.score = 0
        self.all_sprites = pg.sprite.LayeredUpdates()
        self.platforms = pg.sprite.Group()
        self.stars = pg.sprite.Group()
        self.clouds = pg.sprite.Group()
        self.player = Player(self)
        self.all_sprites.add(self.player)
        self.cloud_images = []
        for i in range(1, 4):
            filename = "cloud{}.png".format(i)
            img = pg.image.load(filename)
            self.cloud_images.append(img)
        for i in range(8):
            c = Cloud(self)
            c.rect.x += 500
        for plat in PLATFORM_LIST:
            p = Platform(*plat,self)
            self.all_sprites.add(p)
            self.platforms.add(p)
        self.show_start_screen()
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
                # self.player.jumping = False
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
                    height = rn.randrange(100, 251)
                    x = rn.randrange(WIDTH + 50, WIDTH + 150)
                    width = x - WIDTH
                    #     y = random.randrange(-75,-30)
                    p = Platform(x, HEIGHT - height, width, height, self)
                    self.platforms.add(p)
                    self.all_sprites.add(p)
                    self.player.count = 0
                    self.score += 1
            for clod in self.clouds:
                clod.rect.x -= abs(self.player.vel.x)
                if self.player.count > 50:
                    c = Cloud(self)
                    c.rect.x += 500
        if len(self.clouds) < 6:
            c = Cloud(self)
        if self.player.vel.x < -.05:
            self.player.count -= 1
            if self.player.count < 0:
                self.player.count = 0
        if self.player.rect.left <= WIDTH / 2.5:
            self.player.pos.x += abs(self.player.vel.x)
            for plat in self.platforms:
                plat.rect.x += abs(self.player.vel.x)
        if self.player.rect.left <= WIDTH / 2.5:
            for clod in self.clouds:
                clod.rect.x += abs(self.player.vel.x)

        sta_hits = pg.sprite.spritecollide(self.player,self.stars,True)
        for sta in sta_hits:
            if sta.type == 'boost':
                self.player.vel.y = -(BOOST_POWER//3)
                self.player.vel.x = +BOOST_POWER*2

        if self.player.rect.top > HEIGHT:
            for sprite in self.all_sprites:
                sprite.rect.y -= max(self.player.vel.y, 10)

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
        self.draw_text(self.screen,str(self.score),22,WIDTH//2,15,WHITE)
        # *after* drawing everything, flip the display
        pg.display.flip()

    def show_start_screen(self):
        # game splash/start screen
        self.screen.fill(BLUE)
        time = pg.time.get_ticks()
        for i in range(500):
            self.screen.fill(BLUE)
            self.draw_text(self.screen, 'Bunny hop', 64, 0+i, HEIGHT / 4, WHITE)
        pg.display.flip()
        waiting = True
        while waiting:

            # color = random.choice([RED, WHITE])
            self.draw_text(self.screen, 'Press A to Begin', 18, WIDTH / 2, HEIGHT * 3 / 4, RED)


            pg.display.flip()
            self.clock.tick(FPS)
            for event in pg.event.get():
                keystate = pg.key.get_pressed()
                if event.type == pg.QUIT:
                    pg.quit()
                if event.type == pg.KEYDOWN:
                    if keystate[pg.K_a]:
                        waiting = False

    def show_go_screen(self):
        # game over/continue
        pass

g = Game()
g.show_start_screen()
while g.running:
    g.new()
    g.show_go_screen()

pg.quit()