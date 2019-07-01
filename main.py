import pygame as pg
from pygame.locals import *
import sys
import random

_fps = 60

class Raquet(pg.Surface):
    x = 0
    y = 0
    w = 16
    h = 96
    color = (255, 255, 255)
    velocidad = 15
    diry = 1

    def __init__(self):
        pg.Surface.__init__(self, (self.w, self.h))
        self.fill(self.color)

    def setColor(self, color):
        self.color = color
        self.fill(self.color)

    def avanza(self):
        self.y += self.diry * self.velocidad

        if self.y <=0:
            self.y = 0
 
        if self.y >= 600 - self.h:
            self.y = 600 - self.h


class Ball(pg.Surface):
    x = 0
    y = 0
    w = 16
    h = 16
    color = (255, 255, 255)
    velocidad = 5
    dirx = velocidad
    diry = velocidad

    def __init__(self):
        pg.Surface.__init__(self, (self.w, self.h))
        self.fill(self.color)

    def setColor(self, color):
        self.color = color
        self.fill(self.color)

    def avanza(self):
        if self.x >= 800:
            self.dirx = -self.velocidad
        if self.x <= 0:
            self.dirx = self.velocidad
        if self.y >= 600:
            self.diry = -self.velocidad
        if self.y <= 0:
            self.diry = self.velocidad

        self.x += self.dirx
        self.y += self.diry

    def comprobarChoque(self, candidata):

        if (candidata.x >= self.x and candidata.x <= self.x+self.w or \
           candidata.x+candidata.w >= self.x and candidata.x+candidata.w <= self.x+self.w) and \
           (candidata.y >= self.y and candidata.y <= self.y+self.h or \
            candidata.y+candidata.h >= self.y and candidata.y+candidata.h <= self.y+self.h):

            self.dirx = self.dirx * -1
            self.x += self.dirx


class Game:
    clock = pg.time.Clock()

    def __init__(self, width, height):
        self.size = (width, height)
        self.display = pg.display
        self.screen = self.display.set_mode(self.size)
        self.screen.fill((60, 60, 60))
        self.display.set_caption('Mi juego')

        self.ball1 = Ball()
        self.ball1.setColor((255, 0, 0))
        self.ball1.x = random.randrange(800)
        self.ball1.y = random.randrange(600)
        self.ball1.velocidad = random.randrange(2, 9)

        self.player1 = Raquet()
        self.player1.x = 768
        self.player1.y = 252

    def start(self):
        while True:
            self.clock.tick(_fps)

            for event in pg.event.get():
                if event.type == QUIT:
                    pg.quit()
                    sys.exit()

                if event.type == KEYDOWN:
                    if event.key == K_UP:
                        self.player1.diry = -1
                        self.player1.avanza()

                    if event.key == K_DOWN:
                        self.player1.diry = 1
                        self.player1.avanza()                    

            #Modifica la posición de ball
            self.ball1.avanza()
            self.ball1.comprobarChoque(self.player1)


            #Pintar los sprites en screen
            self.screen.fill((60,60,60))

            self.screen.blit(self.ball1, (self.ball1.x, self.ball1.y))
            self.screen.blit(self.player1, (self.player1.x, self.player1.y))

            self.display.flip()

if __name__ == '__main__':
    pg.init()
    game = Game(800, 600)
    game.start()
