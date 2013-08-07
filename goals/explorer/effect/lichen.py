"""
Overview of the Lichen algorithm

def add_effect(effect, goal = goal):
    if goal is not None:
        1. compute the competence of the goal (as a function of dist(goal, effect))
        2. find a neighborhood of the goal
        3. compute interest over the neighborhood
        4. assign newly computed interest value to the whole neighborhood
    else:
        ...

def next_goal():
    1. choose a past goal proportionaly to its interest
    2. generate a random new point at a distance of the order of the neighborhood radius.

The radius of the neighborhood is a parameter needed. It will define the reachable space
and the neighborhood of a goal. When using LWR, sigma should be the optimum value.
"""
import math
import random
import pandas
import numpy as np

import toolbox
import toolbox.fun
import models
from models.dataset import Databag

from ..tools import competence
from ..tools import interest
from ..tools.meshgrid import Meshgrid

from explorer import GoalExplorer

spread    = 1.0 # How far from the reachable zone can goal be set.
goal_freq = 85

class LichenExplorer(GoalExplorer):
    """Lichen Explorer

    Implementation of the Lichen algorithm for picking new goals
    with a dual mode : effect and goal.

    """

    def __init__(self, Sfeats, R = 5.0):
        """
        @param R  radius of a neighborhood.

        ..note: R should be automatically infered, perhaps on a goal/effect basis.
                Right now, we don't have a good heuristic to determine R. So it is
                set arbitrarily.

        """
        self.dim        = len(Sfeats)
        self.Sfeats     = Sfeats
        self.size       = 0
        self.R          = R

        self.goals      = Databag(self.dim) # goal pursued
        self.effects    = Databag(self.dim) # effects observed

        self.effects_interest = []
        self.goals_interest   = Meshgrid(len(Sfeats), 3, R)
        # this is a meshgrid, as picking proportionnaly out of a sum of gaussian
        # is intractable.

        self.competence = []

    def add_effect(self, effect, goal = None):
        self.size += 1
        effect_bare = effect[list(self.Sfeats)]
        goal_bare   = goal[list(self.Sfeats)] if goal is not None else None
        if goal is not None:
            self._update_goal_interest(goal_bare, effect_bare)
        self._update_effect_interest(goal_bare, effect_bare)

    def _update_goal_interest(self, goal_bare, effect_bare):
        # 1. compute competence
        c = competence.competence(goal_bare, effect_bare)
        if len(self.goals) > 0:
            # 2. find neighborhood
            dists, nhood_idx = self.goals.nn(goal_bare, k = 10)
            #dists, nhood_idx = zip(*[(d, i) for d, i in zip(dists, nhood_idx) if d < 2*self.R])
            # 3. compute interest
            past_c = [self.competence[i] for i in sorted(nhood_idx)] + [c]
            inte = max(0.0, interest.cealled_derivative(past_c))
            # 4. assign interest
            self.goals_interest.add_p(goal_bare, inte)
            # for d, i in zip(dists, nhood_idx):
            #     w = math.exp(-d/(2*self.R*self.R))
            #     self.interest_g[i] = self.interest_g[i]*(1-w) + w*inte#inte
            # #self.interest_g.append(inte)
            # self.interest_g.append(inte)
        else:
            pass
            # self.interest_g.append(0.01) # HACK HACK HACK -> Why not +inf ?
        self.goals.add(goal_bare)
        self.competence.append(c)

    def _set_effect_interest(self, effect_idx):
        effect = self.effects.get(effect_idx)
        dists = self.goals.nn(effect, k = 5)[0]
        dists = [d for d in dists if d < float('inf')]
        d = sum(dists)/len(dists)
        # 2 compute interest
        if d <= self.R:
            self.effects_interest[effect_idx] = 0.0
        else:
            self.effects_interest[effect_idx] = d-self.R


    def _update_effect_interest(self, goal_bare, effect_bare):
        """Update the interest of a new effect"""
        self.effects.add(effect_bare)
        # 1 find nearest goals
        if len(self.goals) == 0:
            self.effects_interest.append(10*self.R) # next motor or sensory babbling
                                              # will be around there.
        else:
            self.effects_interest.append(None)
            self._set_effect_interest(len(self.effects_interest) - 1)
        # 3 override effects'interest in goal neighborhood
        if goal_bare is not None:
            dist, nhood_idx = self.effects.nn(goal_bare, k = 20, radius = self.R) # TODO k = 100 ?
            for d, idx in zip(dist, nhood_idx):
                if d < float('+inf'):
                    self._set_effect_interest(idx)

    def next_goal(self):
        # choose a past goal
        if 100*random.random() < goal_freq:
            return self._mode_goal()
        else:
            return self._mode_effect()

    def _mode_effect(self):
        # choose an past effect
        assert len(self.effects_interest) > 0, "Error : No motor babbling was done to bootstrap the space."
        idx = toolbox.fun.roulette_wheel(self.effects_interest)
        ref_effect = self.effects.get(idx)
        gen_goal = ref_effect + self.R*np.array([random.uniform(-1, 1) for _ in self.Sfeats])
        return pandas.Series(gen_goal, index = self.Sfeats)

    def _mode_goal(self):
        # choose a past goal
        if len(self.goals_interest) == 0:
            assert len(self.effects_interest) > 0
            return self._mode_effect()
        else:
            areas, inte = zip(*[(a, i) for a, i in self.goals_interest.nodes.iteritems()])
            idx = toolbox.fun.roulette_wheel(inte)
            ref_goal = self.goals_interest.res * np.array(areas[idx])
            # generate a random goal
            i = 0
            while (i < 100):
                i += 1
                gen_goal  = ref_goal + spread*self.R*np.array([random.uniform(-1, 1) for _ in self.Sfeats])
                nn_effect = self.effects.get(self.effects.nn(gen_goal, 1)[1][0])
                if True or toolbox.norm(gen_goal, nn_effect) < spread*self.R:
                    return pandas.Series(gen_goal, index = self.Sfeats)
            raise ValueError("Too much tries")
