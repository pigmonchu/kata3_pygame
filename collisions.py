import pygame as pg
from pygame.locals import *
import sys, os
import random

_fps = 60

class Ball(pg.sprite.Sprite):
    x = random.randrange(800)
    y = random.randrange(600)
    velocidad = random.randrange(5, 15)
    dirx = random.choice([-1, 1])
    diry = random.choice([-1, 1])

    def __init__(self):
        pg.sprite.Sprite.__init__(self)

        self.image = pg.image.load(os.getcwd()+"/assets/beach-ball.png")
        self.rect = self.image.get_rect()

    def update(self):
        self.x += self.dirx * self.velocidad
        self.y += self.diry * self.velocidad

        if self.x >= 800:
            self.dirx = -1
            self.x = 800 - self.rect.w
        
        if self.x <= 0:
            self.dirx = 1
            self.x = self.rect.w

        if self.y >= 600:
            self.diry = -1
            self.y = 600 - self.rect.h
        
        if self.y <= 0:
            self.diry = 1
            self.y = self.rect.h

        self.rect.x = self.x
        self.rect.y = self.y
            

    def comprobarChoque(self, spriteGroup):
        if pg.sprite.spritecollide(self, spriteGroup, True):
            if random.choice([0,1]):
                self.dirx = -self.dirx
            else:
                self.diry = -self.diry

class Wall(pg.sprite.Sprite):
    def __init__(self, x, y, w, h):
        pg.sprite.Sprite.__init__(self)

        self.image = pg.Surface((w, h))
        self.image.fill((146, 190, 255))
        self.rect = self.image.get_rect()

        self.rect.x = x
        self.rect.y = y



class Game:
    clock = pg.time.Clock()

    def __init__(self, width, height):
        self.display = pg.display
        self.screen = self.display.set_mode((width, height))
        self.screen.fill((60, 60, 60))
        self.display.set_caption('Paredes')

        self.ball = Ball()
        self.allSprites = pg.sprite.Group()
        self.allSprites.add(self.ball)

        self.wallGroup = pg.sprite.Group()
        for i in range(random.randint(10, 26)):
            w = Wall(random.randrange(800), random.randrange(600), random.randrange(10, 80), random.randrange(10, 80))
            self.wallGroup.add(w)

        self.allSprites.add(self.wallGroup)

    def start(self):
        game_over = False
        while not game_over:
            self.clock.tick(_fps)

            for event in pg.event.get():
                if event.type == QUIT:
                    game_over = True

            self.screen.fill((60, 60, 60))

            self.ball.comprobarChoque(self.wallGroup)

            self.allSprites.update()
            self.allSprites.draw(self.screen)

            self.display.flip()

        pg.quit()
        sys.exit()

if __name__ == '__main__':
    pg.init()
    game = Game(800,600)
    game.start()