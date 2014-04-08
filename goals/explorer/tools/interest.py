"""Function used to compute interest"""

import numpy as np
import forest

import tseries

#raise DeprecationWarning

defcfg = forest.Tree()

defcfg.function = 'theil_sen'
# see desc below

defcfg.min_deriv = 2
defcfg.min_deriv_desc = "number of competence points necessary to compute the derivative"

defcfg.max_deriv = 50
defcfg.max_deriv_desc = "number max of competence points used to compute the derivative"


_functions = {'slidding_window':    tseries.slidding_window,
              'derivative':         tseries.derivative,
              'cealled_derivative': tseries.cealled_derivative
             }
defcfg.function_desc = 'the function used to compute interest (among {})'.format(', '.join(_functions.keys()))

def interest(vector, cfg):
    return _functions[cfg.function](vector, cfg.max_deriv)