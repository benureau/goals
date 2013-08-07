"""Random, no memory babbling module."""

import random

import pandas
import treedict

defaultcfg = treedict.TreeDict()

class MotorBabble(object):

    defaultcfg = defaultcfg

    @classmethod
    def from_robot(cls, robot, cfg = defaultcfg):
        """Create a babbler from a robot instance"""
        cfg.m_bounds = robot.m_bounds
        return cls(robot.m_feats, cfg = cfg)

    def __init__(self, m_feats, m_bounds, cfg = defaultcfg):
        self.m_feats = m_feats
        self.m_bounds = m_bounds
        self.cfg = cfg

        self.n = 0
        self.finished = False

    def babble(self):
        rndpoint = [random.uniform(mi_min, mi_max) for mi_min, mi_max in self.m_bounds]
        return pandas.Series(rndpoint, index = self.m_feats)

    def add_order(self, order, effect = None):
        """Add an executed order, and, optionally, its effect"""
        self.n += 1
        if self.n >= self.cfg.guide.min_orderbabble:
            self.finished = True