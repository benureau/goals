# import matplotlib
# matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import matplotlib.backends.backend_agg as agg
import pygame
import render

plt.ion()

class CellRenderer(render.Renderer):

    def __init__(self, window, cell, size = (300, 700), offset = (0, 0)):
        self.window = window
        self.cell = cell
        if cell is not None:
            self.gcell  = cell.gcell
            self.ecell  = cell.ecell
        self.offset = offset

        figsize = (size[0]/100.0, size[1]/100.0)
        self.figure = plt.figure(figsize = figsize, dpi = 100, facecolor = 'white', edgecolor = 'white')
        self.c_plot   = self.figure.add_subplot(311, title = 'competence')
        self.cp_plot  = self.figure.add_subplot(312, title = 'competence progress')
        self.it_plot  = self.figure.add_subplot(313, title = 'interest')
        # self.pe_plot  = self.figure.add_subplot(413, title = 'prediction error')
        # self.pei_plot = self.figure.add_subplot(414, title = 'prediction error improvement')
        self.figure.subplots_adjust(bottom=0.05, left=0.1, right=0.9, top=0.95, hspace=0.25)

        self.canvas = agg.FigureCanvasAgg(self.figure)
        self.last_draw = None, None

        self.max_n = 0
        self.min_c = 0.0
        self.min_cp, self.max_cp = float('inf'), -float('inf')
        self.max_it = -float('inf')

    def draw(self):
        if self.cell is None:
            return
        if self.last_draw != (self.cell, len(self.cell)):

            self.max_n = max(self.max_n, len(self.cell.c_history))

            if len(self.cell.c_history) > 0:
                self.min_c = min(self.min_c, min(self.cell.c_history))
            self.min_cp = min(self.min_c, min(self.cell.cp_history))
            self.max_cp = max(self.max_cp, max(self.cell.cp_history))
            self.max_it = max(self.max_it, max(self.cell.inst_history))


            self.c_plot.cla()
            self.c_plot.plot(self.cell.c_history, color = (189/255.0, 21/255.0, 80/255.0))
            self.c_plot.set_title('cell {} - competence'.format(self.cell.uid), size = 10)
            self.c_plot.set_xlim(0, self.max_n)
            self.c_plot.set_ylim((self.min_c - 0.1, 0.0))
            self.c_plot.tick_params(labelsize = 8)

            self.cp_plot.cla()
            self.cp_plot.plot(self.cell.cp_history[1:], color = (189/255.0, 21/255.0, 80/255.0))
            self.cp_plot.set_title('cp', size = 10)
            self.cp_plot.set_xlim(0, self.max_n)
            self.cp_plot.set_ylim((self.min_cp - 0.1, self.max_cp + 0.1))
            self.cp_plot.tick_params(labelsize = 8)

            self.it_plot.cla()
            self.it_plot.plot(self.cell.inst_history[1:], color = (189/255.0, 21/255.0, 80/255.0))
            self.it_plot.set_title('interest', size = 10)
            self.it_plot.set_xlim((0, self.max_n))
            self.it_plot.set_ylim((0.0, self.max_it + 0.1))
            self.it_plot.tick_params(labelsize = 8)
            # self.pe_plot.cla()
            # self.pe_plot.plot(self.cell.pe_history, color = (233/255.0,127/255.0,  2/255.0))
            # self.pe_plot.set_title('pe', size = 10)
            # self.pe_plot.tick_params(labelsize = 8)
            # self.pei_plot.cla()
            # self.pei_plot.plot(self.cell.pei_history, color = (233/255.0,127/255.0,  2/255.0))
            # self.pei_plot.set_title('pei', size = 10)
            # self.pei_plot.tick_params(labelsize = 8)

            self.canvas.draw()
            renderer = self.canvas.get_renderer()
            raw_data = renderer.tostring_rgb()

            size = self.canvas.get_width_height()

            self.last_draw = self.cell, len(self.cell)

            self.surf = pygame.image.fromstring(raw_data, size, "RGB")

        pygame.display.get_surface().blit(self.surf, self.offset)
