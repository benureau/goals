import testenv

import forest

from goals import guide
from goals.explorer import effect

def test1():
    """Basic instanciation of Guide"""
    cfg = forest.Tree()
    g = guide.Guide((-1,), (1,), ((-10.0, 10.0),), cfg)

    def f(x):
        return (2*x[0]**1.5,)

    for _ in range(20):
        action = g.next_action()
        if action[0] == 'goal':
            break

    return True

def test2():
    """Basic instanciation of Guide with a GridExplorer"""

    cfg = forest.Tree()
    cfg.effect.s_bounds = ((-64, 64),)
    cfg.effect.s_res    = (25,)

    goalexplorer = effect.GridExplorer((1, ), cfg)
    g = guide.Guide((-1,), (1,), ((-10.0, 10.0),), cfg, goalexplorer = goalexplorer)

    def f(x):
        return (2*x[0]**1.5,)

    for _ in range(20):
        action = g.next_action()
        if action[0] == 'goal':
            break

    return True




tests = [test1,
         test2,
        ]

if __name__ == "__main__":
    print("\033[1m%s\033[0m" % (__file__,))
    for t in tests:
        print('%s %s' % ('\033[1;32mPASS\033[0m' if t() else
                         '\033[1;31mFAIL\033[0m', t.__doc__))