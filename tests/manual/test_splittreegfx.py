import testenv

import random
import time

import goals.explorer.tools.splittree as splittree

render = True
#render = False
bounds   = ((0.0, 2.0), (0.0, 2.0))
min_size = (0.01, 0.01)
st = splittree.SplitTree(bounds, 5, min_size = min_size)

if render:
    import goals.gfx.areas_gfx as areas_gfx
    import goals.gfx.render as render
    window = render.PygameWindow((600, 600))
    strender = areas_gfx.SplitTreeRenderer(window, st, draw_dp = True, offset = (100, 100))
    window.update()

for i in xrange(20):
    time.sleep(0.1)
    x = random.random()
    y = random.random()
    st.add((x, y))
    window.update()

for i in xrange(100):
    st.add((0.4, 0.4))


while True:
    window.update()
    time.sleep(0.1)
    x = random.random()
    y = random.random()
    st.cells_of((x, y))
    st.add((x, y))

