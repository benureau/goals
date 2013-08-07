import testenv

import random
import time

import goals.explorer.effect.cell as cell
from goals.gfx import cell_gfx, render


dcell = cell.DualCell(((-100.0, 100.0),), None, None, w = [1.0])
window = render.PygameWindow((500, 700))
c_gfx = cell_gfx.CellRenderer(window, dcell)
window.renderers.append(c_gfx)

goal = (10.0,)

for i in xrange(100):
    effect     = (10.0 + random.uniform(-(10-i), 10-i),)
    prediction = (10.0 + random.uniform(-(10-i), 10-i),)

    dcell.add(effect, goal = goal, prediction = prediction)

    window.update()
    time.sleep(0.1)
raw_input()