import pygame
import render

class PointCloudRenderer(render.Renderer):

    def __init__(self, window, bounds, points, color = (0, 0, 0), size = (400, 400), offset = (0, 0), margin = 10):
        render.Renderer.__init__(self, window, size = size, offset = offset, margin = margin)

        self.bounds = bounds
        self.points = points
        self.color = color

        self.x_min  = bounds[0][0]
        self.width  = bounds[0][1] - self.x_min
        self.y_min  = bounds[1][0]
        self.height = bounds[1][1] - self.y_min

    def draw(self):
        for p in self.points:
            if p is not None:
                x0, y0 = self.coo2screen(p[0], p[1])
                pygame.draw.circle(self.canvas, self.color, (int(x0), int(y0)), 2)