import testenv

import treedict

import goals
from goals.explorer.effect.rndexpl import BoundedRandomExplorer


def test1():
    """Basic instanciation of BoundedRandomExplorer"""
    cfg = treedict.TreeDict()
    cfg.effect.s_bounds = ((-1, 1), (0, 10))

    bre = BoundedRandomExplorer((0, 1), cfg = cfg)
    for i in range(10):
        g = bre.next_goal()
        bre.add_effect(g, g)
    return True

tests = [test1]

if __name__ == "__main__":
    print("\033[1m%s\033[0m" % (__file__,))
    for t in tests:
        print('%s %s' % ('\033[1;32mPASS\033[0m' if t() else
                         '\033[1;31mFAIL\033[0m', t.__doc__))
