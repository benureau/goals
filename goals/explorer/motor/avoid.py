import random
import pandas

class MotorBabble(object):

    @classmethod
    def from_robot(cls, robot):
        """Create a babbler from a robot instance"""
        return cls(robot.m_feats, robot.m_bounds)

    def __init__(self, m_feats, m_bounds):
        self.m_feats = m_feats
        self.m_bounds = m_bounds

    def babble(self, *args):
        rndpoint = [random.uniform(mi_min, mi_max) for mi_min, mi_max in self.m_bounds]
        return pandas.Series(rndpoint, index = self.m_feats)

    def add_order(self, order, effect = None):
        """Add an executed order, and, optionally, its effect"""
        pass