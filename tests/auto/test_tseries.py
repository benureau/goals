import testenv

import random
random.seed(123)

import goals.explorer.tools.tseries as tseries
import cgoals

# tse = tseries.TheilSenEstimator()
# se  = tseries.SeigelEstimator()
# cse  = cgoals.cSeigelEstimator(20)
#
# data = []
#
# for i in range(20):
#     if i == 4:
#         v = random.uniform(0, 2000)
#     else:
#         v  = i + random.uniform(-2, 2)
#     data.append(v)
#     tse.add(v)
#     se.add(v)
#     cse.add(v)
#
# print se.value()
# print cse.value()
# print tse.value()
# print tseries.derivative(data)
# print tseries.slidding_window(data)

# tse  = tseries.TheilSenEstimator()
# se  = tseries.SeigelEstimator()
# cse = cgoals.cSeigelEstimator(20)
# for d in [-6.663405279634873, -3.8683377753465584, -7.29871873842211]:
#     cse.add(d)
#     tse.add(d)
#     se.add(d)
#
# print cse.value()
# print tse.value()
# print se.value()

def test1():
    """Testing if python and C++ implementation of Seigel yield the same results"""
    check = True


    for _ in range(100):
        se  = tseries.SeigelEstimator()
        sse  = tseries.SpanSeigelEstimator(20)
        cse = cgoals.cSeigelEstimator(20)

        size = random.randint(2, 20)
        data = [random.uniform(-10, 10) for _ in xrange(size)]

        for i, d  in enumerate(data):
            cse.add(d)
            sse.add(d)
            se.add(d)
            if abs(cse.value() - se.value()) > 0.01:
                check = False
                print cse.value()
                print sse.value()
                print se.value()
                print data[:(i+1)]

    return check

tests = [test1]

if __name__ == "__main__":
    print("\033[1m%s\033[0m" % (__file__,))
    for t in tests:
        print('%s %s' % ('\033[1;32mPASS\033[0m' if t() else
                         '\033[1;31mFAIL\033[0m', t.__doc__))