import pygame as pg
import numpy as np
import os

from lab4.sprites import Model


class GoatFrontRightLeg(Model):

    def __init__(self):
        super().__init__()
        self.image = pg.image.load(os.path.join("sprite", "goat", "front_right_leg.png")).convert_alpha()
        self.rotateCenter = (27, 25)


class GoatFrontLeftLeg(Model):

    def __init__(self):
        super().__init__()
        self.image = pg.image.load(os.path.join("sprite", "goat", "front_left_leg.png")).convert_alpha()
        self.rotateCenter = (27, 25)


class GoatBackRightLeg(Model):

    def __init__(self):
        super().__init__()
        self.image = pg.image.load(os.path.join("sprite", "goat", "back_right_leg.png")).convert_alpha()
        self.rotateCenter = (27, 25)


class GoatBackLeftLeg(Model):

    def __init__(self):
        super().__init__()
        self.image = pg.image.load(os.path.join("sprite", "goat", "back_left_leg.png")).convert_alpha()
        self.rotateCenter = (34,27)


class Goat(Model):

    def __init__(self):
        super().__init__()
        self.image = pg.image.load(os.path.join("sprite", "goat", "body.png")).convert_alpha()
        self.imagePrime = pg.image.load(os.path.join("sprite", "goat", "goat.png"))

        self.legAngles = [80, 0, 0, -5]
        self.legPositions = [(284, 295),(238, 299),(116, 289),(80, 250)]
        self.legs = [
            GoatFrontLeftLeg(),
            GoatFrontRightLeg(),
            GoatBackLeftLeg(),
            GoatBackRightLeg()
        ]

        self.rotateCenter = (205,228)

    def renderOn(self, surface: pg.Surface, rotate, point, scale=(1,1), rotateCenter=None):
        sf = pg.Surface(self.imagePrime.get_size(), pg.SRCALPHA)
        sf.blit(self.image, (46, 0))

        for i,leg in enumerate(self.legs):
            leg.renderOn(sf,self.legAngles[i],self.legPositions[i])

        if rotateCenter == None:
            rotateCenter = self.rotateCenter

        sf, dest = self.getRotationAndShift(sf, rotateCenter, rotate, point)
        sf, offset = self.getScale(sf, scale=scale)
        surface.blit(sf, dest+offset)


if __name__ == "__main__":
    pg.init()

    FPS = 30
    screen = pg.display.set_mode((800, 530))

    goat = Goat()

    dest = screen.get_size()

    clock = pg.time.Clock()
    finished = False
    # main cycle

    angle = 0
    while not finished:
        clock.tick(FPS)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                finished = True
            if event.type == pg.MOUSEBUTTONDOWN:
                pass
        angle += 10
        screen.fill(pg.Color("#000000"))
        goat.renderOn(screen, angle, np.asarray(dest) / 2 + np.asarray((100*np.sin(angle/10/np.pi), 0)), (1+np.sin(angle/10/np.pi), 1))
        pg.display.flip()

    pg.quit()