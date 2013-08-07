
import pygame
import render
import cell_gfx

from point_gfx import PointCloudRenderer
from areas_gfx import GridRenderer

class GridExplorerRenderer(render.Renderer):

    def __init__(self, window, grid, datalog = None, size = (800, 800), offset = (0, 0), margin = 10):
        render.Renderer.__init__(self, window, size = size, offset = offset, margin = margin)

        self.window = window
        sub_size = ((self.size[0] - 100)/2, (self.size[1] - 100)/2)
        g_offset = (offset[0], offset[1] + sub_size[1] + 100)
        p_offset = (offset[0] + sub_size[0] + 100, offset[1])

        self.datalog = datalog
        if self.datalog is not None:
            self.effects     = PointCloudRenderer(window, grid.bounds, datalog.effects,     color = (138,155, 15), size = sub_size, offset =   offset, margin = margin)
            self.goals       = PointCloudRenderer(window, grid.bounds, datalog.goals,       color = (189, 21, 80), size = sub_size, offset = g_offset, margin = margin)
            #self.predictions = PointCloudRenderer(window, grid.bounds, datalog.predictions, color = (233,127,  2), size = sub_size, offset = p_offset, margin = margin)

        self.grid = grid
        self.cellgfx = cell_gfx.CellRenderer(self.window, None, size = (400, 700), offset = (1000, 100))
        self.e_st = GridRenderer(window, self.grid, cell_gfx = self.cellgfx, size = sub_size, offset =   offset, margin = margin, color = (150, 150, 150))
        self.g_st = GridRenderer(window, self.grid, cell_gfx = self.cellgfx, size = sub_size, offset = g_offset, margin = margin, color = (150, 150, 150), draw_interest = True)
        #self.p_st = GridRenderer(window, self.grid, cell_gfx = self.cellgfx, size = sub_size, offset = p_offset, margin = margin, color = (150, 150, 150), draw_interest = True)


    def draw(self):
        self.e_st.draw()
        self.g_st.draw()
        #self.p_st.draw()
        if self.cellgfx is not None:
           self.cellgfx.draw()

        if self.datalog is not None:
            self.effects.draw()
            self.goals.draw()
            #self.predictions.draw()
