import pygame as pg
from pygame.locals import *
import sys, os
import random

_fps = 60

def between(valor, liminf, limsup):
    return liminf <= valor <= limsup

class Raquet(pg.sprite.Sprite):
    x = 0
    y = 0
    w = 16
    h = 96
    color = (255, 255, 255)
    velocidad = 5
    velocidadMax = 15
    diry = 1

    def __init__(self, sigueA=None):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((self.w, self.h))
        self.image.fill(self.color)
        self.sigueA = sigueA

        self.rect = self.image.get_rect()

    def pointInit(self):
        self.y = (600 - self.h) // 2

    def avanza(self, acelera=None):
        if acelera:
            self.velocidad = min(self.velocidadMax, self.velocidad+acelera)

        self.y += self.diry * self.velocidad

        if self.y <=0:
            self.y = 0
 
        if self.y >= 600 - self.h:
            self.y = 600 - self.h

    def update(self):
        if self.sigueA:
            if abs(self.sigueA.x - self.x) <= 65:
                if not between(self.sigueA.y, self.y, self.y+self.h):
                    self.diry = (self.sigueA.y - self.y) / abs(self.sigueA.y - self.y)
                    self.avanza(1)

        self.rect.x = self.x
        self.rect.y = self.y
        

    def esComputer(self):
        if self.sigueA:
            return True
        return False


class Ball(pg.sprite.Sprite):
    x = 0
    y = 0
    w = 16
    h = 16
    color = (255, 255, 255)
    velocidadIni = 5
    dirx = 1
    diry = 1
    raquetazos = 0

    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((self.w, self.h))
        self.image.fill((255, 255, 255))
        self.image.set_colorkey((255, 255, 255))
        pg.draw.circle(self.image, (250, 250, 250), (self.w//2,self.w//2), self.w//2)
        self.rect = self.image.get_rect()

        self.sound = pg.mixer.Sound(os.getcwd()+'/assets/ping.wav')
        self.lost = pg.mixer.Sound(os.getcwd()+'/assets/lost-point.wav')

        self.velocidadX = self.velocidadIni
        self.velocidadY = self.velocidadIni

    def posicion_saque(self, ganador):
        self.x = 392
        self.y = 292
        self.diry = random.choice([-1,1])

        if ganador == 1:
            self.dirx = -1
        else:
            self.dirx = 1
        self.velocidadX = 0
        self.velocidadY = 0
        raquetazos = 0

    def start(self):
        self.velocidadX = self.velocidadIni
        self.velocidadY = self.velocidadX

    def avanza(self):
        if self.x >= 800:
            self.lost.play()
            self.posicion_saque(1)
            return 2

        if self.x <= 0:
            self.lost.play()
            self.posicion_saque(2)
            return 1

        return None 

    def update(self):
        if self.y >= 584:
            self.diry = -1
        if self.y <= 0:
            self.diry = 1

        self.x += self.dirx * self.velocidadX
        self.y += self.diry * self.velocidadY

        self.rect.x = self.x
        self.rect.y = self.y

    def comprobarChoque(self, spriteGroup):
        if pg.sprite.spritecollide(self, spriteGroup, False):
            self.dirx = self.dirx * -1
            self.x += self.dirx
            semivelocidad = max(self.velocidadY // 2, 1)
            self.velocidadY = random.randrange(semivelocidad, 4 * semivelocidad)

            self.sound.play()

            self.raquetazos += 1
            if self.raquetazos >= 3:
                self.velocidadX += 1
                self.raquetazos = 0                


    def comprobarChoque1(self, candidata):
        if (between(self.y, candidata.y, candidata.y+candidata.h) or between(self.y+self.h, candidata.y, candidata.y+candidata.h)) and \
           (between(self.x, candidata.x, candidata.x+candidata.w) or between(self.x+self.w, candidata.x, candidata.x+candidata.w)):
            self.dirx = self.dirx * -1
            self.x += self.dirx

            self.sound.play()


class Game:
    clock = pg.time.Clock()
    puntuaciones = {1: 0, 2: 0}
    winScore = 15
    winner = None

    def __init__(self, width, height):
        self.size = (width, height)
        self.display = pg.display
        self.screen = self.display.set_mode(self.size)
        self.screen.fill((60, 60, 60))
        self.display.set_caption('Mi juego')

        self.ball1 = Ball()

        self.player1 = Raquet()
        self.player1.x = 772

        self.player2 = Raquet(self.ball1)
        self.player2.x = 12
        
        self.playersGroup = pg.sprite.Group()
        self.allGroup = pg.sprite.Group()

        self.playersGroup.add(self.player1)
        self.playersGroup.add(self.player2)
        self.allGroup.add(self.playersGroup)
        self.allGroup.add(self.ball1)

        self.fuente = pg.font.Font(os.getcwd()+'/assets/font.ttf', 48)
        self.iniciopartida()
        
    def iniciopartida(self):
        self.ball1.posicion_saque(random.choice([1,2]))
        self.ball1.start()
        self.player1.pointInit()
        self.player2.pointInit()

        self.puntuaciones[1] = 0
        self.puntuaciones[2] = 0

        self.winner = None

        self.marcador1 = self.fuente.render(str(self.puntuaciones[1]), 1, (255, 255, 255))
        self.marcador2 = self.fuente.render(str(self.puntuaciones[2]), 1, (255, 255, 255))


    def gameover(self):
        pg.quit()
        sys.exit()

    def handleevent(self):
        for event in pg.event.get():
            if event.type == QUIT:
                self.gameover() 

            # Controlamos pulsaciones de teclas
            if event.type == KEYDOWN:
                if event.key == K_UP:
                    self.player1.diry = -1
                    self.player1.velocidad = 5
                    self.player1.avanza()

                if event.key == K_DOWN:
                    self.player1.diry = 1
                    self.player1.velocidad = 5
                    self.player1.avanza()

                if event.key == K_q and not self.player2.esComputer():
                    self.player2.diry = -1
                    self.player2.velocidad = 5
                    self.player2.avanza()

                if event.key == K_a and not self.player2.esComputer():
                    self.player2.diry = 1
                    self.player2.velocidad = 5
                    self.player2.avanza()

                if event.key == K_SPACE:
                    if self.winner:
                        self.iniciopartida()
                    self.ball1.start()

        # Controlamos teclas mantenidas
        keys_pressed = pg.key.get_pressed()
        if keys_pressed[K_UP]:
            self.player1.diry = -1
            self.player1.avanza(1)

        if keys_pressed[K_DOWN]:
            self.player1.diry = 1
            self.player1.avanza(1)                

        if keys_pressed[K_q]:
            self.player2.diry = -1
            self.player2.avanza(1)

        if keys_pressed[K_a]:
            self.player2.diry = 1
            self.player2.avanza(1)                

    def recalculate(self):
        #Modifica la posición de ball y comprueba sus
        p = self.ball1.avanza()
        if p:
            self.puntuaciones[p] += 1
            self.marcador1 = self.fuente.render(str(self.puntuaciones[1]), 1, (255, 255, 255))
            self.marcador2 = self.fuente.render(str(self.puntuaciones[2]), 1, (255, 255, 255))
            self.ball1.posicion_saque(p)
            self.player1.pointInit()
            self.player2.pointInit()

            if self.puntuaciones[1] >= self.winScore or self.puntuaciones[2] >= self.winScore:
                self.winner = self.fuente.render("Ganador jugador {}".format(p), 1, (255, 255, 0))
                    

        self.ball1.comprobarChoque(self.playersGroup)

    def render(self):
        #Pintar los sprites en screen
        self.screen.fill((60,60,60))

        self.allGroup.update()
        self.allGroup.draw(self.screen)
        self.screen.blit(self.marcador2, (32, 8))
        self.screen.blit(self.marcador1, (720, 8))

        if self.winner:
            rect = self.winner.get_rect()
            self.screen.blit(self.winner, ((800 - rect.w)//2, (600 - rect.h) // 2) )

        

        self.display.flip()

    def start(self):
        while True:
            self.clock.tick(_fps)

            self.handleevent()

            self.recalculate()

            self.render()

if __name__ == '__main__':
    pg.init()
    game = Game(800, 600)
    game.start()
