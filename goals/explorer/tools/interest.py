"""Function used to compute interest"""

import numpy as np
import treedict

import tseries

#raise DeprecationWarning

defaultcfg = treedict.TreeDict()

defaultcfg.function = 'theil_sen'
# see desc below

defaultcfg.min_deriv = 2
defaultcfg.min_deriv_desc = "number of competence points necessary to compute the derivative"

defaultcfg.max_deriv = 50
defaultcfg.max_deriv_desc = "number max of competence points used to compute the derivative"


_functions = {'slidding_window':    tseries.slidding_window,
              'derivative':         tseries.derivative,
              'cealled_derivative': tseries.cealled_derivative
             }
defaultcfg.function_desc = 'the function used to compute interest (among {})'.format(', '.join(_functions.keys()))

def interest(vector, cfg):
    return _functions[cfg.function](vector, cfg.max_deriv)