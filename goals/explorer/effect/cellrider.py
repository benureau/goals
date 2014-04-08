from __future__ import print_function, division
import numbers
import collections
import random

import forest
import toolbox

from celltree import CellTree

defcfg = forest.Tree()

defcfg._describe('effect.random_explo', instanceof=numbers.Real,
                 docstring='Percentage (between 0.0 and 1.0) of random goal exploration')

defcfg._describe('effect.unknown_explo', instanceof=numbers.Real,
                 docstring='Percentage (between 0.0 and 1.0) of exploration of areas with effect but no goal')

defcfg._describe('effect.sample_size', instanceof=numbers.Integral,
                 docstring='How many goals to pick per region at minimum regardless of the interest measure')

defcfg._describe('effect.s_bounds', instanceof=collections.Iterable,
                 docstring='The min/max bounds of each sensory features')

defcfg._describe('effect.crit_size', instanceof=numbers.Integral,
                 docstring='Size at which a cell splits')

class CellRider(object):

    def __init__(self, cfg, w = None):
        self.cfg = cfg
        self.cfg.update(defcfg, overwrite = False, protect_structure = True)

        self.bounds = self.cfg.effect.s_bounds
        assert self.bounds is not None

        self.celltree = CellTree(self.bounds, cfg.cell.crit_size, cfg, w = w)

    def __len__(self):
        return len(self.celltree)

    def add_effect(self, effect, goal = None, prediction = None, competence = None, pred_error = None):
        self.celltree.add(effect, goal = goal, prediction = prediction, competence = competence, pred_error = pred_error)

    def next_goal(self):

        target_cell = None
        dice = random.random()

        if dice < self.cfg.effect.random_explo:
            target_cell = random.sample(self.celltree.active_cells, 1)[0]

        # elif dice < self.cfg.effect.random_explo + self.cfg.effect.unknown_explo:
        #     target_cell = self._priority_choice()

        if target_cell is None:
            target_cell = self._priority_choice()

        if target_cell is None:
            cell_uid = [cell.uid for cell in self.celltree.active_cells]
            interests = [cell.interest() for cell in self.celltree.active_cells]
            if sum(interests) > 0:
                idx = toolbox.roulette_wheel(interests)
                priority_uid = [cell.uid for cell in self.celltree.active_cells]
                target_cell = self.celltree.cells[priority_uid[idx]]

        if target_cell is not None:
            return target_cell.random_point()
        else:
            return None

    def _priority_choice(self):
        target_cell = None
        priority_uid = [cell.uid for cell in self.celltree.active_cells]
        priorities   = [self._priority(cell) for cell in self.celltree.active_cells]
        if sum(priorities) > 0:
            idx = toolbox.roulette_wheel(priorities)
            target_cell = self.celltree.cells[priority_uid[idx]]

        return target_cell


    def _priority(self, cell):
        if len(cell.ecell) > 0:
            return max(3 - len(cell.gcell), 0)
        else:
            return 0
