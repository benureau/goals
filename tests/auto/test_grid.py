import testenv

import random, sys

import forest

from goals.explorer.effect import grid

def test1():
    """Test basic methods of gridexplorer"""

    cfg = forest.Tree()
    cfg.effect.s_bounds = ((0.0, 1.0), (0.0, 1.0))

    ge = grid.GridExplorer((0, 1), cfg = cfg)

    for _ in xrange(100):
        effect     = (random.random(), random.random())
        goal       = (random.random(), random.random())
        prediction = (random.random(), random.random())
        ge.add_effect(effect, goal = goal, prediction = prediction)

    for _ in xrange(1000):
        ge.next_goal()

    ge.cell_list()
    ge.active_cell_list()

    return True

tests = [test1]

if __name__ == "__main__":
    print("\033[1m%s\033[0m" % (__file__,))
    for t in tests:
        print('%s %s' % ('\033[1;32mPASS\033[0m' if t() else
                         '\033[1;31mFAIL\033[0m', t.__doc__))


