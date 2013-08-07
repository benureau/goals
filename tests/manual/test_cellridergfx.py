import testenv

import random, sys, time

import treedict

from goals.explorer import datalog
from goals.explorer.effect import cellrider
import goals.gfx.cellrider_gfx as cellrider_gfx
import goals.gfx.render as render

cfg = treedict.TreeDict()
cfg.s_bounds = ((0, 1), (0, 1))
cfg.crit_size = 10

cr = cellrider.CellRider(cfg = cfg)

window = render.PygameWindow((1500, 1000))
dl = datalog.DataLog(None)
crrender = cellrider_gfx.CellRiderRenderer(window, cr, dl, offset = (100, 100))
window.renderers.append(crrender)

for _ in xrange(100):
    effect     = (random.random(), random.random())
    goal       = (random.random(), random.random())
    prediction = (random.random(), random.random())
    dl.manual_feedback(effect, goal = goal, prediction = prediction)
    cr.add_effect(effect, goal = goal, prediction = prediction)
    window.update()

while True:
    cr.next_goal()
    window.update()
    time.sleep(0.1)
