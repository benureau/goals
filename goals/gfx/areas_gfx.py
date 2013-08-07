import threading
import random
import time

import pygame
import matplotlib as plt

import render

cmap = plt.cm.get_cmap('Blues')

class AreasRenderer(render.Renderer):

    def __init__(self, window, explorer, cell_gfx = None, draw_dp = False, draw_interest = False, size = (400, 400), color = (0, 0, 0), offset = (0, 0), margin = 10):
        render.Renderer.__init__(self, window, size = size, offset = offset, margin = margin)

        self.explorer = explorer
        self.draw_dp = draw_dp
        self.color = color
        self.draw_interest = draw_interest
        assert len(self.explorer.bounds) == 2 # we only support 2D.

        self.x_min  = self.explorer.bounds[0][0]
        self.width  = self.explorer.bounds[0][1] - self.x_min
        self.y_min  = self.explorer.bounds[1][0]
        self.height = self.explorer.bounds[1][1] - self.y_min

        self.cell_gfx = cell_gfx

    def draw(self):
        raise NotImplementedError

    def _draw_datapoint(self, dp):
        x0, y0 = self.coo2screen(dp[0], dp[1])
        pygame.draw.circle(self.canvas, (255, 0, 0), (int(x0), int(y0)), 2)


    def mouseMoved(self, x_s, y_s):
        if self.belongs(x_s, y_s):
            x, y = self.screen2coo(x_s, y_s)
            self.cell_gfx.cell = self.point2cell(x, y)
            return True
        return False

    def point2cell(self, x, y):
        raise NotImplementedError

def zeroone(v, min_v, max_v):
    if min_v == max_v:
        return 0.0
    return (float(v) - min_v)/(max_v - min_v)

class GridRenderer(AreasRenderer):

    def draw(self):
        if self.draw_interest:
            interests = [cell.interest() for cell in self.explorer.cells]
            min_int = min(interests)
            max_int = max(interests)


        for cell in self.explorer.cells:
            x0, y0 = self.coo2screen(cell.bounds[0][0], cell.bounds[1][0])
            x1, y1 = self.coo2screen(cell.bounds[0][1], cell.bounds[1][1])

            rect = pygame.Rect(x0, y0, x1-x0+1, y1-y0+1)

            if self.draw_interest:
                c = cmap(zeroone(cell.interest(), min_int, max_int))
                c = (255.0*c[0], 255.0*c[1], 255.0*c[2])
                pygame.draw.rect(self.canvas, c, rect)

            pygame.draw.rect(self.canvas, self.color, rect, 1)

    def point2cell(self, x, y):
        return self.explorer.point2cell((x, y))


class SplitTreeRenderer(AreasRenderer):

    def _draw_split(self, region):
        if not region.leaf:
            if region.div == 0:
                x0, y0 = self.coo2screen(region.cutoff, region.bounds[1][0])
                x1, y1 = self.coo2screen(region.cutoff, region.bounds[1][1])
            else:
                x0, y0 = self.coo2screen(region.bounds[0][0], region.cutoff)
                x1, y1 = self.coo2screen(region.bounds[0][1], region.cutoff)

            pygame.draw.line(self.canvas, self.color, (x0, y0), (x1, y1))

            for child in region.children:
                self._draw_split(child)

    def draw(self):
        self._draw_tree(self.explorer)
        if self.draw_dp:
            for datapoint in self.explorer.datapoints:
                self._draw_datapoint(datapoint)

    def _draw_tree(self, region = None):
        if region is None:
            region = self.explorer
        x0, y0 = self.coo2screen(region.bounds[0][0], region.bounds[1][0])
        x1, y1 = self.coo2screen(region.bounds[0][1], region.bounds[1][1])

        rect = pygame.Rect(x0, y0, x1-x0, y1-y0)
        pygame.draw.rect(self.canvas, self.color, rect, 1)

        self._draw_split(region)

    def point2cell(self, x, y):
        return self.explorer.leaf_of((x, y))
