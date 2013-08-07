""" Module defining class and methods for computation on sequences
    (such as competence and prediction error histories)
"""

import numbers
import numpy as np

import toolbox

class TheilSenEstimator(object):

    def __init__(self):
        self.sequence = []
        self.slopes = []
        self.beta = 0.0
        self.last_compute = 0
        self.size = 0

    def add(self, value):
        assert isinstance(value, numbers.Number)
        value = float(value)
        self.sequence.append(value)
        self.size += 1

    def _recompute(self):
        for n in range(self.last_compute, self.size):
            value = self.sequence[n]
            self.slopes.append([])
            for i in range(n):
                v_i = self.sequence[i]
                self.slopes[i].append((value - v_i)/(n - i))
        self.beta = np.median(np.fromiter(toolbox.flatten(self.slopes), float, count = -1))

    def value(self, span = None):
        if self.last_compute < len(self.sequence):
            self._recompute()
        return self.beta

class SeigelEstimator(object):

    def __init__(self):
        self.sequence = []
        self.slopes = []
        self.beta = 0.0
        self.last_compute = 0
        self.size = 0

    def add(self, value):
        assert isinstance(value, numbers.Number)
        value = float(value)
        self.sequence.append(value)
        self.size += 1

    def _recompute(self, span = None):
        if span is not None:
            span = min(self.size, span)
        for n in range(self.last_compute, self.size):
            value = self.sequence[n]
            self.slopes.append([])
            for i in range(n):
                v_i = self.sequence[i]
                slope_i = (value - v_i)/(n - i)
                self.slopes[i].append(slope_i)
                self.slopes[n].append(slope_i)
        if span is None:
            medians = [np.median(slopes_i) for slopes_i in self.slopes]
            self.beta = np.median(medians)
        else:
            medians = [np.median(self.slopes[i][-span:]) for i in range(-span, 0)]
        self.last_compute = self.size

    def value(self, span = None):
        if self.last_compute < len(self.sequence):
            self._recompute(span)
        return self.beta

class SpanSeigelEstimator(object):

    def __init__(self, span):
        self.sequence = []
        self.slopes = []
        self.beta = 0.0
        self.span = span
        self.last_compute = 0
        self.size = 0

    def add(self, value):
        assert isinstance(value, numbers.Number)
        value = float(value)
        self.sequence.append(value)
        self.size += 1
        self.last_compute = max(self.last_compute, self.size - self.span)

    def _recompute(self):
        for n in range(self.last_compute, self.size):
            value = self.sequence[n]
            self.slopes.append([])
            for i in range(max(0, self.size-self.span), n):
                v_i = self.sequence[i]
                slope_i = (value - v_i)/(n - i)
                self.slopes[i].append(slope_i)
                self.slopes[n].append(slope_i)

        span = min(self.size, self.span)
        medians = [np.median(self.slopes[i][-span:]) for i in range(-span+1, 0)]
        self.beta = np.median(medians)
        self.last_compute = self.size

    def value(self):
        if self.last_compute < len(self.sequence):
            self._recompute()
        return self.beta

# Non-robust obsolete methods

def derivative(vector):
    """ Treat the vector as a time serie of uniform timesteps, and returns
        the first order derivative of it.
    """
    n = len(vector)
    X = np.matrix([[1 for _ in xrange(n)],
                   range(n)
                  ])
    y = np.matrix(vector)
    B = (np.linalg.pinv(X*X.T)*X)*y.T
    return B[1, 0]

def cealled_derivative(vector, maxc = 0.0):
    """ Same as derivative, but with a special case when competence is perfect.
        :arg maxc:  the maximum competence. Competence is assumed to go lower as
                    reaching precision decreases.
    """
    n = len(vector)
    X = np.matrix([[1 for _ in xrange(n)],
                   range(n)
                  ])
    y = np.matrix(vector[-n:])
    B = (np.linalg.pinv(X*X.T)*X)*y.T
    origin = B[0, 0]
    slope = B[1, 0]
    possible = max(0.0, maxc - (slope*(len(vector)-1) + origin))
    return min(slope, possible)

def slidding_window(vector, tw = float('inf')):
    """Compute the interest of the experiences using the "mean time window" metric
        :arg  vector:  competence value of exp in chronological order.
        :arg  tw:      time window : how many competences values to consider.
    """
    n = len(vector)
    tw = min(tw, n)
    if tw == 0:
        return 0.0
    beta = (sum(vector[n-tw/2:n]) - sum(vector[n-tw:n-tw/2+1]))/(tw*tw/4)
    return beta
