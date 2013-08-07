import math
import random

import treedict

import toolbox

from ..tools import cmpce
from cgoals import cSeigelEstimator as SpanSeigelEstimator
#from ..tools.tseries import SpanSeigelEstimator

defaultcfg = treedict.TreeDict()

defaultcfg.cell.min_cp  = 3
defaultcfg.cell.min_cp_desc = "number of competence points necessary to compute the derivative (competence progress)"

defaultcfg.cell.min_pei = 3
defaultcfg.cell.min_pei_desc = "number of effect points necessary to compute the derivative (prediction error improvement)"

defaultcfg.cell.max_cp  = 20
defaultcfg.cell.max_pei = 20

defaultcfg.cell.threshold_cp  = 0.02
defaultcfg.cell.threshold_pei = 0.02

defaultcfg.cell.factor_cp  = True
defaultcfg.cell.factor_pei = False


class DualCell(object):

    def __init__(self, bounds, graph, uid, cfg, depth = 0, w = None):
        self.gcell =   GoalCell(bounds, graph, uid, cfg, depth = depth, w = w)
        self.ecell = EffectCell(bounds, graph, uid, cfg, depth = depth, w = w)
        self.leaf  = True
        self.inst_history = [0.0]

    def add_goal(self, effect, goal, competence = None):
        self.gcell.add(goal, effect)
        self.inst_history.append(self.interest())

    def add_effect(self, effect, prediction = None, pred_error = None):
        return self.ecell.add(effect, prediction)

    def add(self, effect, goal = None, prediction = None, competence = None, pred_error = None):
        self.gcell.add(goal, effect)
        active = self.ecell.add(effect, prediction)

        self.inst_history.append(self.interest())

        return active

    def split(self, low_bounds, high_bounds):
        self.leaf = False
        low_cell  = DualCell(low_bounds,  self.graph, None, self.cfg, depth = self.depth + 1,
                             w = self.w)
        high_cell = DualCell(high_bounds, self.graph, None, self.cfg, depth = self.depth + 1,
                             w = self.w)

        low_active, high_active = False, False
        for effect, prediction, pred_error in zip(self.ecell.effects,
                                                 self.ecell.predictions,
                                                 self.ecell.pe_history):
            low_active  +=  low_cell.add(effect, prediction = prediction, pred_error = pred_error)
            high_active += high_cell.add(effect, prediction = prediction, pred_error = pred_error)

        for effect, goal, competence in zip(self.gcell.effects,
                                            self.gcell.goals,
                                            self.gcell.c_history):
            low_active  +=  low_cell.add(effect, goal = goal, competence = competence)
            high_active += high_cell.add(effect, goal = goal, competence = competence)

        self.graph.split(self, low_cell, high_cell)

    def __len__(self):
        return len(self.ecell) + len(self.gcell)

    def __getattr__(self, name):
        try:
            return getattr(self.ecell, name)
        except AttributeError:
            return getattr(self.gcell, name)

    def interest(self):
        inst = 1.0
        if self.cfg.cell.factor_pei:
            abs_pei = self.pei
            if abs_pei < 0:
                abs_pei = abs(abs_pei)/2.0
            if pei < 0.02:
                abs_pei = 0.0
            inst *= abs_pei
        if self.cfg.cell.factor_cp:
            abs_cp = self.cp
            if abs_cp < 0:
                abs_cp = abs(abs_cp)/2.0
            if abs_cp < 0.02:
                abs_cp = 0.0
            inst *= abs_cp
        return inst

    def interest_all(self):
        """Not optimized ! Don't call this often yet."""
        inst = 1.0
        if self.cfg.cell.factor_pei:
            abs_pei = self.pei_all
            if abs_pei < 0:
                abs_pei = abs(abs_pei)/2.0
            if pei < 0.02:
                abs_pei = 0.0
            inst *= abs_pei
        if self.cfg.cell.factor_cp:
            abs_cp = self.cp_all
            if abs_cp < 0:
                abs_cp = abs(abs_cp)/2.0
            if abs_cp < 0.02:
                abs_cp = 0.0
            inst *= abs_cp
        return inst


class Cell(object):

    def __init__(self, bounds, graph, uid, cfg, depth = 0, w = None):
        """
            :arg graph:  container structure for the cell.
                         is called when splits happen.
            :arg uid:    unique id for the cell
            :arg w:      list of weights for each dimension
        """
        self.bounds    = bounds
        self.graph     = graph
        self.uid       = uid
        self.w         = w
        self.depth     = depth

        self.effects     = []

        self.cfg       = cfg
        cfg.update(defaultcfg, overwrite = False)

    # def exploration_interest(self):
    #     """ Return how interesting is it to create a goal in a new, unknown area.
    #         Will be > 0 iff an effect has been observed in the cell, and a not
    #         too much goals have been set previously in the area.
    #     """
    #     return max(self.cfg.sample_size - len(self.c_history), 0)

    def random_point(self):
        return tuple(random.uniform(min_i, max_i) for min_i, max_i in self.bounds)

    def belongs(self, point):
        return all(min_pi <= pi <= max_pi for pi, (min_pi, max_pi) in zip(point, self.bounds))

class EffectCell(Cell):

    def __init__(self, bounds, graph, uid, cfg, depth = 0,  w = None):
        """"""
        Cell.__init__(self, bounds, graph, uid,  depth = depth, w = w, cfg = cfg)

        self.predictions = []

        self.pe_history    = []    # PE : Prediction Error
        self.pei_history   = [0.0] # PEI: PE Improvement
        self.estimator_pei = SpanSeigelEstimator(cfg.cell.max_pei)

    def add(self, effect, prediction = None, pred_error = None):

        if not self.belongs(effect):
            return False

        self.effects.append(effect)

        if prediction is not None or pred_error is not None:
            self.predictions.append(prediction)
            if pred_error is None:
                pred_error = cmpce.competence(prediction, effect, cfg = self.cfg)

            self.pe_history.append(pred_error)
            self.estimator_pei.add(pred_error)

            if len(self.pe_history) >= self.cfg.cell.min_pei:
                self.pei_history.append(self.estimator_pei.value())
            else:
                self.pei_history.append(0.0)

        return True

    def split(self, low_bounds, high_bounds):
        return self.graph.effect_split(self, low_bounds, high_bounds)

    @property
    def pe(self):
        return self.pe_history[-1]

    @property
    def pei(self):
        return self.pei_history[-1]

    @property
    def pei_all(self):
        if len(self.pe_history) < 2:
            return 0.0
        estimator = SpanSeigelEstimator(len(self.pe_history))
        for pe in self.pe_history:
            if pe is not None:
                estimator.add(pe)
        return estimator.value()

    def avg_pred_error(self, span = None):
        if len(self.pe_history) == 0:
            return None
        if span is not None and span > 0:
            return sum(self.pe_history[:-span])/span
        else:
            return sum(self.pe_history)/len(self.pe_history)

    def __len__(self):
        return len(self.effects)

class GoalCell(Cell):

    def __init__(self, bounds, graph, uid, cfg, depth = 0, w = None):
        """"""
        Cell.__init__(self, bounds, graph, uid, depth = depth, w = w, cfg = cfg)

        self.goals       = []

        self.c_history     = []    # C  : Competence
        self.cp_history    = [0.0] # CP : Competence Progress
        self.estimator_cp  = SpanSeigelEstimator(cfg.cell.max_cp)

    def add(self, goal, effect, competence = None):

        if goal is None or not self.belongs(goal):
            return

        self.goals.append(goal)
        self.effects.append(effect)

        if competence is None:
            competence = cmpce.competence(goal, effect, cfg = self.cfg)

        self.c_history.append(competence)
        self.estimator_cp.add(competence)

        if len(self.c_history) >= self.cfg.cell.min_cp:
            self.cp_history.append(self.estimator_cp.value())
        else:
            self.cp_history.append(0.0)

    def split(self, low_bounds, high_bounds):
        return self.graph.goal_split(self, low_bounds, high_bounds)

    @property
    def competence(self):
        return self.c_history[-1]

    @property
    def cp_all(self):
        if len(self.c_history) < 2:
            return 0.0
        estimator = SpanSeigelEstimator(len(self.c_history))
        for c in self.c_history:
            if c is not None:
                estimator.add(c)
        return estimator.value()

    @property
    def cp(self):
        return self.cp_history[-1]

    def avg_competence(self, span = None):
        if len(self.c_history) == 0:
            return None
        if span is not None and span > 0:
            return sum(self.c_history[:-span])/span
        else:
            return sum(self.c_history)/len(self.c_history)

    def __len__(self):
        return len(self.goals)
