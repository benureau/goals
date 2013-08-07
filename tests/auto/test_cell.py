import testenv

import random
import treedict

import goals.explorer.effect.cell as cell
from goals.gfx import cell_gfx


def test1():
    """Check basic cell behavior"""
    cfg = treedict.TreeDict()

    dcell = cell.DualCell(((-100.0, 100.0),), None, None, cfg, w = [1.0])

    goal = (10.0,)

    for i in xrange(40):
        effect     = (10.0 + random.uniform(-(10-i), 10-i),)
        prediction = (10.0 + random.uniform(-(10-i), 10-i),)

        dcell.add(effect, goal = goal, prediction = prediction)

    dcell.gcell.cp_all
    dcell.ecell.pei_all
    dcell.interest_all()

    check = len(dcell.gcell) == 40 and len(dcell.ecell) == 40
    return check

tests = [test1]

if __name__ == "__main__":
    print("\033[1m%s\033[0m" % (__file__,))
    for t in tests:
        print('%s %s' % ('\033[1;32mPASS\033[0m' if t() else
                         '\033[1;31mFAIL\033[0m', t.__doc__))

# c_gfx = cell_gfx.CellRenderer(gc, ec)
# c_gfx.draw()
#
# raw_input()