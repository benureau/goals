import testenv

import random, sys

import treedict

from goals.explorer import datalog
from goals.explorer.effect import grid
import goals.gfx.gridexpl_gfx as gridexplorer_gfx
import goals.gfx.render as render

cfg = treedict.TreeDict()
cfg.s_bounds = ((0, 1), (0, 1))
cfg.s_res    = (10, 10)

cr = grid.GridExplorer((1, 3), cfg = cfg)

window = render.PygameWindow((1500, 1000))
dl = datalog.DataLog(None)
crrender = gridexplorer_gfx.GridExplorerRenderer(window, cr, dl, offset = (100, 100))
window.renderers.append(crrender)

for _ in xrange(100):
    for _ in xrange(5):
        effect     = (random.random(), random.random())
        goal       = (random.random(), random.random())
        prediction = (random.random(), random.random())
        dl.manual_feedback(effect, goal = goal, prediction = prediction)
        cr.add_effect(effect, goal = goal, prediction = prediction)
    window.update()

for _ in xrange(1000):
    sys.stdout.flush()
    cr.next_goal()
    window.update()

raw_input()