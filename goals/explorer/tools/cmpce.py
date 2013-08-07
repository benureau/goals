# -*- coding: utf-8 -*-
"""Regroup different functions to compute interest from a vector of competence values"""

import math
import numpy as np

import treedict

import toolbox

defaultcfg = treedict.TreeDict()

defaultcfg.cmpce.min_d     = 0.0
defaultcfg.cmpce.min_d_desc = "minimum distance. below this value, we have perfect competence (= 0)."

defaultcfg.cmpce.exp_alpha = 2.0
defaultcfg.cmpce.exp_alpha_desc = "alpha for exp competence, as in c = exp(-alpha*d)"

defaultcfg.cmpce.log_beta  = 0.05
defaultcfg.cmpce.log_beta_desc = "beta for log competence, as in c = log(beta + d)"

defaultcfg.cmpce.function = 'log'
defaultcfg.cmpce.function_desc = 'the function used to measure competence. possible values are log|exp|ident'

def competence_log(a, b, min_d, beta):
    """Return the competence as -log(d+1)"""
    d = toolbox.norm(a, b)
    if d <=  min_d:
        d = 0.0
    return -math.log((beta + d)/beta)

def competence_ident(a, b, min_d):
    """Return the competence as d = b-a"""
    d = toolbox.norm(a, b)
    if d <=  min_d:
        d = 0.0
    return -d

def competence_exp(a, b, min_d, alpha):
    """Return the competence as exp(-d)-1"""
    return math.exp(alpha*competence_ident(a,b,min_d))

def competence(a, b, cfg):
    """Default competence"""
    assert len(a) == len(b)
    cfg.update(defaultcfg, overwrite = False)

    if cfg.cmpce.function == 'log':
        return competence_log(a, b, cfg.cmpce.min_d, cfg.cmpce.log_beta)
    elif cfg.cmpce.function == 'exp':
        return competence_exp(a, b, cfg.cmpce.min_d, cfg.cmpce.exp_alpha)
    elif cfg.cmpce.function == 'ident':
        return competence_ident(a, b, cfg.cmpce.min_d)
    else:
        raise ValueError, "Unknown competence <{}>".format(cfg.cmpce.function)

    return competence_log(a, b)
