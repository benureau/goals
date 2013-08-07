import testenv

import random
import time

random.seed(123)

import goals.explorer.tools.tseries as tseries
import cgoals

tse = tseries.TheilSenEstimator()
se  = tseries.SeigelEstimator()
sse  = tseries.SpanSeigelEstimator(20)
cse  = cgoals.cSeigelEstimator(20)

# preparing data
data = []
for i in range(1000):
    if i == 4:
        v = random.uniform(0, 2000)
    else:
        v  = i + random.uniform(-2, 2)
    data.append(v)


t0 = time.time()
data0 = [0., 1., 2.]
for d in data:
    data0.append(d)
    tseries.derivative(data0)
t0 = time.time() - t0

t1 = time.time()
data1 = [0., 1., 2.]
for d in data:
    data1.append(d)
    tseries.slidding_window(data1)
t1 = time.time() - t1

# t2 = time.time()
# for d in data:
#     tse.add(d)
#     tse.value()
# t2 = time.time() - t2

t3 = time.time()
se.add(0.0)
se.add(1.0)
se.add(2.0)
for d in data:
    se.add(d)
    se.value(20)
t3 = time.time() - t3

t4 = time.time()
sse.add(0.0)
sse.add(1.0)
sse.add(2.0)
for d in data:
    sse.add(d)
    sse.value()
t4 = time.time() - t4

t5 = time.time()
cse.add(0.0)
cse.add(1.0)
cse.add(2.0)
for d in data:
    cse.add(d)
    cse.value()
t5 = time.time() - t5

print t0
print t1
print t3
print t4
print t5