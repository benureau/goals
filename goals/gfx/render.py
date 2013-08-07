import threading
import time

import pygame

class PygameWindow(object):

    def __init__(self, size = (400, 400)):
        pygame.init()

        self.size = size
        self.canvas = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)

        self.renderers = []

    def update(self):
        event = pygame.event.poll()
        if event.type == pygame.QUIT:
            exit()
        elif event.type == pygame.MOUSEMOTION:
            for r in self.renderers:
                r.mouseMoved(event.pos[0], event.pos[1])

        self.canvas.fill((255, 255, 255))
        for r in self.renderers:
            r.draw()
        pygame.display.flip()

class Renderer(object):

    def __init__(self, window, size = (400, 400), offset = (0, 0), margin = 10):
        self.size      = size
        self.offset    = offset
        self.margin    = margin

        window.renderers.append(self)
        self.canvas = window.canvas

    def coo2screen(self, x, y):
        x_p, y_p = (x-self.x_min)/self.width, (y-self.y_min)/self.height
        x_s = round(x_p*(self.size[0] - 2*self.margin) + self.margin)
        y_s = round(y_p*(self.size[1] - 2*self.margin) + self.margin)
        return int(self.offset[0] + x_s), int(self.offset[1] + y_s)

    def screen2coo(self, x_s, y_s):
        x_s, y_s = float(x_s - self.offset[0]), float(y_s - self.offset[1])
        x = (x_s - self.margin)/(self.size[0] - 2*self.margin)
        y = (y_s - self.margin)/(self.size[1] - 2*self.margin)
        x = x*self.width  + self.x_min
        y = y*self.height + self.y_min
        x = min(self.x_min+self.width, max(self.x_min, x))
        y = min(self.y_min+self.height, max(self.y_min, y))
        return x, y

    def mouseMoved(self, x, y):
        return False

    def belongs(self, x_s, y_s):
        return (self.offset[0] + self.margin <= x_s <= self.offset[0] - self.margin + self.size[0]
            and self.offset[1] + self.margin <= y_s <= self.offset[1] - self.margin + self.size[1])
