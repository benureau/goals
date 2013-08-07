import testenv
import random

import treedict

from goals.explorer.effect import celltree

def test1():
    """Test basic method"""
    bounds = ((-1.0, 1.0), (-1.0, 1.0))
    cfg = treedict.TreeDict()
    ct = celltree.CellTree(bounds, 5, cfg)

    for i in xrange(100):
        effect     = (random.uniform(-1, 1), random.uniform(-1, 1))
        goal       = (random.uniform(-1, 1), random.uniform(-1, 1))
        prediction = (random.uniform(-1, 1), random.uniform(-1, 1))
        ct.add(effect, goal, prediction)

    return True

tests = [test1]

if __name__ == "__main__":
    print("\033[1m%s\033[0m" % (__file__,))
    for t in tests:
        print('%s %s' % ('\033[1;32mPASS\033[0m' if t() else
                         '\033[1;31mFAIL\033[0m', t.__doc__))