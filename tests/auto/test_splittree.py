import testenv

import random
import time

import goals.explorer.tools.splittree as splittree

def test1():
    """Test if basic methods don't raise errors"""
    bounds   = ((0.0, 2.0), (0.0, 2.0))
    min_size = (0.01, 0.01)
    st = splittree.SplitTree(bounds, 5, min_size = min_size)

    for i in xrange(20):
        x = random.random()
        y = random.random()
        st.add((x, y))

    for i in xrange(100):
        st.add((0.4, 0.4))

    for i in xrange(100):
        x = random.random()
        y = random.random()
        st.cells_of((x, y))
        st.add((x, y))

    return True

tests = [test1]

if __name__ == "__main__":
    print("\033[1m%s\033[0m" % (__file__,))
    for t in tests:
        print('%s %s' % ('\033[1;32mPASS\033[0m' if t() else
                         '\033[1;31mFAIL\033[0m', t.__doc__))