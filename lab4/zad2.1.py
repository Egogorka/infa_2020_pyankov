import pygame as pg
from pygame.draw import *

import numpy as np

from lab4.sprites import Model, Animation
from lab4.goat import Goat
from lab4.goatAnimation import GoatAnimation


def drawParabola(surface: pg.Surface, color: pg.Color, r0: tuple, r1: tuple, f: lambda x: x):
    """
    Функция, рисующая параболу
    :param surface: Surface - поверхность, на которой рисуется парабола
    :param color: Color - цвет параболы
    :param r0: Tuple (x,y) - координаты левой границы параболы
    :param r1: Tuple (x,y) - координаты правой границы параболы
    :param f: lambda - лямбда-функция, описывающая параболу
    :return:
    """
    ls = getParabolaList(r0[0], r1[0], f)
    ls.append(r1)
    ls.append(r0)
    polygon(surface, color, ls)


def getParabolaList(x0: int, x1: int, f: lambda x: x) -> list:
    """
    Функция, состявляющия лист точек графика параболы, задаваемой f, от x0 до x1
    :type f: lambda
    """
    ls = []
    for i in range(x0, x1, 1):
        ls.append((i, int(f(i))))
    return ls


def drawBackground(surface: pg.Surface) -> None:
    """
    Функция рисует фон картинки
    :param surface: Surface - поверхность, на которой рисуется фон
    :return: None
    """

    rect(surface, (254, 214, 163), (0, 0, 800, 530))
    rect(surface, (254, 214, 197), (0, 110, 800, 230))
    circle(surface, (252, 239, 27), (400, 50), 40)


def drawTopMounains(surface: pg.Surface, color: pg.Color) -> None:
    """
    Функция рисует верхние горы
    :param surface: Surface - поверхность, на которой рисуются горы
    :param color: Color - цвет гор
    :return: None
    """

    polygon(surface, color,
            [(165, 108), (196, 119), (205, 140), (307, 204), (360, 195), (387, 209), (165, 230)])
    polygon(surface, color,
            [(387, 209), (429, 107), (463, 182), (480, 161), (480, 200)])

    drawParabola(surface, color, (480, 200), (600, 189), lambda x: (-25 / 3481) * (x - 480) ** 2 + 161)
    drawParabola(surface, color, (0, 245), (165, 230), lambda x: (-109 / 21904) * (x - 17) ** 2 + 217)

    polygon(surface, color,
            [(579, 105), (634, 134), (666, 127), (718, 155), (750, 140), (800, 170), (600, 189)])


def drawBottomMountains(surface: pg.Surface, color: pg.Color) -> None:
    """
    Функция рисования нижних гор
    :param surface: Surface - поверхность, на которую рисуем горы
    :param color: Color - цвет гор
    :return:
    """
    polygon(surface, color,
            [(800, 190), (800, 340), (655, 344), (655, 284), (688, 240), (720, 263), (740, 235), (770, 240)])
    polygon(surface, color,
            [(459, 284), (459, 350), (140, 360), (140, 340), (175, 282), (231, 311), (260, 240), (325, 255),
             (385, 300)])
    polygon(surface, color,
            [(0, 250), (25, 264), (25, 360), (0, 360)])

    drawParabola(surface, color, (25, 360), (140, 360), lambda x: (18 / 841) * (x - 73) ** 2 + 214)
    drawParabola(surface, color, (450, 360), (565, 360), lambda x: (1 / 125) * (x - 550) ** 2 + 220)
    drawParabola(surface, color, (565, 360), (655, 360), lambda x: (-59 / 7921) * (x - 655) ** 2 + 285)


def drawFloor(screen: pg.Surface, color: pg.Color):
    """
    Функция рисования "передней" части фона, "пол"
    :param screen: Surface - поверхность, на которой рисуется
    :param color: Color - цвет пола
    :return:
    """

    polygon(screen, color,
            [(0, 358), (800, 340), (800, 530), (0, 530)])
    polygon(screen, color, [(0, 358), (800, 340), (800, 530), (0, 530)])


def drawFrontMountains(screen: pg.Surface, color: pg.Color):
    polygon(screen, color, [(0, 200), (95, 300), (175, 400), (175, 530), (0, 530)])
    polygon(screen, color, [(315, 525), (380, 528), (510, 450), (545, 470), (545, 530), (315, 530)])

    drawParabola(screen, color, (175, 530), (315, 530), lambda x: (-5 / 784) * (x - 315) ** 2 + 525)
    drawParabola(screen, color, (545, 530), (800, 530), lambda x: (-9 / 3380) * (x - 700) ** 2 + 500)


# init
pg.init()

FPS = 30
screen = pg.display.set_mode((800, 530))

drawBackground(screen)
drawTopMounains(screen, pg.Color("#FC9831"))
drawBottomMountains(screen, pg.Color("#AC4334"))
drawFloor(screen, pg.Color("#B38694"))
drawFrontMountains(screen, pg.Color("#2C0721"))

pg.display.update()
clock = pg.time.Clock()
finished = False

goat = Goat()
goatAnimate = GoatAnimation(goat)

goat.renderOn(screen, 0, (119, 389), (120, 120))

sign = lambda t: 2 * np.floor(2 * t - 2 * np.floor(t)) - 1
sawtooth = lambda t: (t - np.floor(t) - 1 / 2) * sign(t)

x1, y1 = (lambda i: 150 * sawtooth(i) + 400, lambda i: -100 * sawtooth(i) + 500)
x2, y2 = (lambda i: 500 * sawtooth(i) + 400, lambda i: -10 * sawtooth(i) + 340)
x3, y3 = (lambda i: 700 * sawtooth(i) + 300, lambda i: -50 * sawtooth(i) + 210)

screen_backup = pg.Surface(screen.get_size())
screen_backup.blit(screen, (0, 0))

# main cycle
time = 0
while not finished:
    clock.tick(FPS)
    time += 0.01
    for event in pg.event.get():
        if event.type == pg.QUIT:
            finished = True
        if event.type == pg.MOUSEBUTTONDOWN:
            print(event.pos)
    screen.blit(screen_backup, (0, 0))
    goatAnimate.angle = 45 * sign(time)
    goatAnimate.renderWalkOn(screen, (x1(time), y1(time)), 3 * time, size=(100, 100), scale=(sign(time), 1))
    goatAnimate.angle = 0
    goatAnimate.renderWalkOn(screen, (x2(time * 3 / 7 + 10), y2(time * 3 / 7 + 10)), 3 * time, size=(40, 40),
                             scale=(sign(time * 3 / 7), 1))
    goatAnimate.angle = 0
    goatAnimate.renderWalkOn(screen, (x3(time * 2 / 17 + 10), y3(time * 2 / 17 + 10)), 2 * time, size=(40, 40),
                             scale=(sign(time * 2 / 17), 1))
    pg.display.flip()

pg.quit()
