# 3 steps:
#   1. cython fmodel.pyx  -> fmodel.cpp
#   2. link: python setup.py build_ext --inplace  -> fmodel.so, a dynamic library
#   3. python test.py

import numpy as np
cimport numpy as np

cdef extern from "c_tseries.h":
    cdef cppclass _cSeigel:
        _cSeigel(int)

        void add(double v)
        double beta()
        int size()

cdef class cSeigelEstimator:

    cdef _cSeigel *thisptr      # hold a C++ instance which we're wrapping

    def __cinit__(self, int span):
        self.thisptr = new _cSeigel(span)

    def __dealloc__(self):
        pass

    # def reset(self):
    #     self.thisptr.reset()

    def add(self, double v):
        self.thisptr.add(v)

    def value(self):
        return self.thisptr.beta()
