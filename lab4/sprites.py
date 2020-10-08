import pygame as pg
import numpy as np


def rotateAroundPoint(surface : pg.Surface, point, rotate)->pg.Surface:
    offset = np.asarray(point) - np.asarray(surface.get_size())/2
    size = np.array(surface.get_size())+2*abs(offset)

    print("offset", offset)

    sf = pg.Surface(size, pg.SRCALPHA)
    dest = - offset + abs(offset)

    sf.blit(surface, dest)
    sf = pg.transform.rotate(sf, rotate)
    return sf

class Animation():
    """
    Has one major method: renderAnimationOn(surface, point, time)
    time is a real number in [0,1]
    time = 0 - start of the animation
    time = 1 - end of it
    """
    def renderAnimationOn(self, surface : pg.Surface, point, time):
        pass



class Model():

    def __init__(self):
        self.image = pg.Surface((1,1), pg.SRCALPHA)
        self.rotateCenter = (0,0)

    def getSurface(self, scale=np.asarray((1,1)))-> pg.Surface:
        """
        :param scale: - расширение, необязательный параметр
        :return: Surface - поверхность, на которой модель
        """
        pass

    def renderOn(self, surface, rotate, point, scale=(1,1), rotateCenter=None):
        """
        Функция рендеринта модели на поверхности

        :param surface: - поверхность, на которой рисуется модель
        :param rotate: - угол, на который модель будет повёрнута
        :param point: - точка, где будет рисоваться модель на поверхности. Совпадает с центром вращения
        :param scale: - расширение, необязательный параметр
        :param rotateCenter: - точка, вокруг которой происходит поворот. Стандатно задана в самой модели
        :return:
        """
        print(self.__class__)
        if rotateCenter == None:
            rotateCenter = self.rotateCenter

        sf, dest = self.getRotationAndShift(self.image, rotateCenter, rotate, point)
        surface.blit(sf, dest)

    def getRotationAndShift(self, surface, rotateCenter, rotate, point)->(pg.Surface, tuple):
        sf = rotateAroundPoint(surface, rotateCenter, rotate)
        dest = np.asarray(point) - np.asarray(sf.get_size()) / 2
        return (sf, dest)

    def getScale(self, surface : pg.Surface, size=None, scale=(1,1) )->(pg.Surface, tuple):
        if size == None:
            size = (int(surface.get_width()*scale[0]),int(surface.get_height()*scale[1]))

        sf = pg.transform.scale(surface, (int(size[0]),int(size[1])))
        dest = ((surface.get_width() - size[0])/2, (surface.get_height() - size[1])/2)
        return (sf, dest)
