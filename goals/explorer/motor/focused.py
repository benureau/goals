"""
Focused motor module.

This module will do random babbling until producing an effect (ie, an non-null vector).
Then, it will do a small burst of babbling around the motor order that produced the effect.
"""

import random
import pandas

class FocusedMotorBabble(object):

    @classmethod
    def from_robot(cls, robot):
        """Create a babbler from a robot instance"""
        return cls(robot.m_feats, robot.m_bounds)

    def __init__(self, m_feats, m_bounds, burst_length = None, near_ratio = 100, **kwargs):
        self.m_feats = m_feats
        self.m_bounds = m_bounds
        self.burst_length = burst_length or max(1, int(len(m_feats)/2))
        self.near_ratio = near_ratio
        self.burst_dist = sum((mi_max-mi_min)/self.near_ratio for mi_min, mi_max in self.m_bounds)

        self.history = {} # key: effect, value:order
        self.nburst = 0
        self.burst = 0
        self.burst_order = None
        self.finished = False

    def babble(self, *args):
        if self.burst == 0:
            order = [random.uniform(mi_min, mi_max) for mi_min, mi_max in self.m_bounds]
            return pandas.Series(order, index = self.m_feats)
        else:
            return self.babble_near_order(self.burst_order)

    def babble_near_order(self, order):
        close_order = [random.uniform(max(mi_min, o_i-mi_min/self.near_ratio), min(mi_max, o_i+mi_max/self.near_ratio))
                       for o_i, (mi_min, mi_max) in zip(order, self.m_bounds)]
        return pandas.Series(close_order, index = self.m_feats)

    def babble_near_effect(self, effect):
        """The effect should be in memory"""
        order = self.history[tuple(effect)]
        return self.babble_near_order(order)

    def add_order(self, order, effect = None):
        """Add an executed order, and, optionally, its effect"""
        if effect is not None:
            self.history[tuple(effect)] = order

        if self.burst > 0:
            if sum(abs(o_i - bo_i) for o_i, bo_i in zip(order, self.burst_order)) <= self.burst_dist:
                self.burst -= 1
                if self.burst == 0:
                    self.nburst += 1
        else:
            if self.burst == 0 and sum(abs(e_i) for e_i in effect) > 0.1:
                self.burst = self.burst_length
                self.burst_order = order

        if self.nburst >= 1:
            self.finished = True