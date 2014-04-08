import random

import forest
import pandas

from toolbox import gfx

from explorer import EffectExplorer

class RandomExplorer(EffectExplorer):

    def __init__(self, s_feats, cfg = None):
        self.dim = len(s_feats)
        self.s_feats   = s_feats
        self.size = 0
        self.extremum = tuple([None, None] for f in s_feats)
        self.welldefined = False
        # As long as we don't have bounds describing an hyperrectangle, we
        # draw goal from the unitary hyperrectangle.

    def next_goal(self):
        if not self.welldefined:
            goal = tuple(random.random() for _ in self.s_feats)
        else:
            goal = tuple(random.uniform(extmin, extmax)
                         for extmin, extmax in self.extremum)
        return pandas.Series(goal, index = self.s_feats)

    def add_effect(self, effect, goal = None, prediction = None):
        """Add an realised effect."""
        self.size += 1
        for effi, exti in zip(effect, self.extremum):
            exti[0] = effi if exti[0] is None else min(effi, exti[0])
            exti[1] = max(effi, exti[1])
        if not self.welldefined:
            self.welldefined = all(extmin<extmax
                                   for extmin, extmax in self.extremum)


defcfg = forest.Tree()

defcfg['effect.s_bounds'] = None
defcfg['effect.s_bounds_desc'] = "the bounds of the sensory features"

class BoundedRandomExplorer(RandomExplorer):

    def __init__(self, s_feats, cfg = None):
        self.dim = len(s_feats)
        self.s_feats   = s_feats
        self.size = 0
        if cfg is None:
            cfg = forest.Tree()
        cfg._update(defcfg, overwrite = False)

        if cfg.effect._get('s_bounds', None) is None:
            print("You must define the cfg.s_bounds parameter for BoundedRandomExplorer")
        assert len(cfg.effect.s_bounds) == self.dim, "{}cfg.s_bounds doesn't have the correct dimension; got {}, expected {}{}".format(gfx.red, len(cfg.effect.s_bounds), self.dim, gfx.end)
        self.bounds = cfg.effect.s_bounds

    def next_goal(self):
        goal = tuple(random.uniform(gi_min, gi_max) for gi_min, gi_max in self.bounds)
        return pandas.Series(goal, index = self.s_feats)

    def add_effect(self, effect, goal = None, prediction = None):
        """Add an realised effect."""
        self.size += 1
        pass
