import pygame as pg
import numpy as np
import os

from lab4.sprites import Model, Animation
from lab4.goat import Goat, GoatFrontRightLeg, GoatFrontLeftLeg, GoatBackRightLeg, GoatBackLeftLeg

class GoatAnimation(Animation):

    def __init__(self, model : Goat):
        Animation.__init__(self, model)
        self.model = model
        self.legs = model.legs
        self.angle = 0

    def renderWalkOn(self, surface: pg.Surface, point, time, size=None, scale=(1, 1)):
        if size == None:
            size = (abs(int(surface.get_width()*scale[0])),abs(int(surface.get_height()*scale[1])))

        self.rotateLegs(time)
        self.model.renderOn(surface, self.angle, point, size, scale)

    def rotateLegs(self, time):

        front_left = self.model.getLeg(Goat.FRONT_LEFT)
        back_left  = self.model.getLeg(Goat.BACK_LEFT)

        front_right = self.model.getLeg(Goat.FRONT_RIGHT)
        back_right = self.model.getLeg(Goat.BACK_RIGHT)

        back_left["angle"] = front_left["angle"] = 40 * np.sin(2 * np.pi * time)
        back_right["angle"] = front_right["angle"] = -40 * np.sin(2 * np.pi * time)

        self.model.setLeg(Goat.FRONT_LEFT, front_left)
        self.model.setLeg(Goat.BACK_LEFT, back_left)

        self.model.setLeg(Goat.FRONT_RIGHT, front_right)
        self.model.setLeg(Goat.BACK_RIGHT, back_right)


if __name__ == "__main__":
    pg.init()

    FPS = 30
    screen = pg.display.set_mode((1600, 1000))
    clock = pg.time.Clock()
    finished = False

    goat = Goat()
    goatAnimation = GoatAnimation(goat)

    dest = screen.get_size()

    # main cycle
    sound = pg.mixer.Sound(os.path.join("sound.wav"))


    time = 0
    while not finished:
        clock.tick(FPS)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                finished = True
            if event.type == pg.MOUSEBUTTONDOWN:
                pass
        time += 0.05
        screen.fill(pg.Color("#000000"))
        # sound.play()
        sound.set_volume((1+np.sin(time))/2)
        # goat.renderOn(screen, angle, np.asarray(dest) / 2 + np.asarray((100*np.sin(angle/10/np.pi), 0)), (1+np.sin(angle/10/np.pi), 1))
        goatAnimation.renderWalkOn(screen,
                                   -60 * np.asarray((np.sin(time**2),np.cos(time))) + np.asarray(dest) / 2 + np.asarray((300,0)),
                                   time ** (1/2), scale=(2+2*np.sin(time**(1/2)),2+2*np.sin(time**(2/3))))

        goatAnimation.renderWalkOn(screen,
                                   60 * np.asarray((np.sin(time ** 2), -np.cos(time**2))) + np.asarray(dest) / 2,
                                   time ** 2, scale=(2+2 * np.cos(time**2),2+ 2 * np.cos(time**2)))

        pg.display.flip()

    pg.quit()