"""EffectExplorer base class

This module is the core of the intrinsic motivation algorithm in the task
space.

An EffectExplorer role is to provide the next goal to try to reach for.
Each time a goal was pursued, the goal/effect pair is given to the
EffectExplorer, so that it can update its internal structures and provide
more relevant futur goals.

It is notable that a EffectExplorer is completely unaware of the motor spaces
of the robot.

When the robot is doing babbling in the motor space without goal, the add_effect()
method can be used without providing a goal. This is important, since the EffectExplorer
needs to bootstrap its estimation of the task space (and, particularly, current
purported boundaries) before any call to next_goal can be made. Since the processing of
the observation can be significantly different whether a goal is provided or not, one
should always provide a goal if it is available.

"""

class EffectExplorer(object):
    """'Abstract interface shared by Explorer classes"""

    def __init__(self, s_feats):
        """
        @param dim     dimension of the sensory features
        @param s_feats  the sensory features
        @param size    the number of effect observed
        """
        self.dim = len(s_feats)
        self.s_feats = s_feats
        self.size = 0

    def next_goal(self):
        """Generate a new goal

        The goal is a vector of length self.dim, which each value corresponding
        to the target values for the feature vector self.s_feats.
        """
        raise NotImplementedError('You need to override next_goal() in child classes')

    def add_effect(self, effect, goal = None, prediction = None):
        """Add an goal, and the actual effect obtained"""
        raise NotImplementedError('You need to override next_goal() in child classes')

    def __len__(self):
        return self.size


class CellEffectExplorer(EffectExplorer):
    """Effect explorer with regions"""

    def cell_list(self):
        """Return a list of region uid"""
        return self.cells

    def active_cell_list(self):
        """Return a list of region uid"""
        return self.active_cells

    def point2cell(self, point):
        """Return the region uid of the given effect"""
        raise NotImplementedError('You need to override regions() in child classes')
