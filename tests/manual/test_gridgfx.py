import testenv

import random
import time

import forest

import goals.explorer.effect.grid as grid

cfg = forest.Tree()
cfg.s_bounds = ((0.0, 2.0), (0.0, 2.0))
cfg.s_res    = (10, 10)
ge = grid.GridExplorer((1,2), cfg = cfg)

import goals.gfx.areas_gfx as areas_gfx
import goals.gfx.render as render
window = render.PygameWindow((600, 600))
strender = areas_gfx.GridRenderer(window, ge, draw_dp = True, offset = (100, 100))
window.update()

for i in xrange(20):
    time.sleep(0.1)
    x = random.random()
    y = random.random()
    ge.add_effect((x, y))
    window.update()

for i in xrange(100):
    ge.add_effect((0.4, 0.4))

while True:
    window.update()
    time.sleep(0.1)
    x = random.random()
    y = random.random()
    ge.add_effect((x, y))

