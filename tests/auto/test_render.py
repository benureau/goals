import testenv
import random

from goals.gfx import render

class DummyWindow(object):
    def __init__(self):
        self.renderers = []
        self.canvas    = None

def test1():
    """Test coordinates conversion"""
    check = True

    w = DummyWindow()
    r = render.Renderer(w, size = (400, 400), offset = (100, 200), margin = 10)

    r.x_min  = 4.0
    r.y_min  = 40.0
    r.width  = 4.0
    r.height = 40.0

    for _ in range(100):
        x = random.randint(110, 490)
        y = random.randint(210, 590)
        x_c, y_c = r.screen2coo(x, y)
        x2, y2 = r.coo2screen(x_c, y_c)
        check *= abs(x - x2) < 0.1 and abs(y - y2) < 0.1


    return check

tests = [test1]

if __name__ == "__main__":
    print("\033[1m%s\033[0m" % (__file__,))
    for t in tests:
        print('%s %s' % ('\033[1;32mPASS\033[0m' if t() else
                         '\033[1;31mFAIL\033[0m', t.__doc__))