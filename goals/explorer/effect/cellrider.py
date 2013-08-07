
import random

import treedict

import toolbox

from celltree import CellTree

defaultcfg = treedict.TreeDict()

defaultcfg.effect.random_explo = 0.05
defaultcfg.effect.random_explo_desc = "Percentage of random goal exploration"

defaultcfg.effect.unknown_explo = 0.10
defaultcfg.effect.unknown_explo_desc = "Percentage of exploration of areas with no goal but effect"

defaultcfg.effect.sample_size = 3
defaultcfg.effect.sample_size_desc = "how many goal to pick per region at minimum regardless of the interest measure"

defaultcfg.effect.s_bounds = None
defaultcfg.effect.s_bounds = "the limit of the sensory features"

defaultcfg.effect.crit_size = 10
defaultcfg.effect.crit_size_desc = "size at which a cell splits"

# defaultcfg.weight_vector = None
# defaultcfg.weight_vector_desc = "size at which a cell splits"

class CellRider(object):

    def __init__(self, cfg, w = None):
        self.cfg = cfg
        self.cfg.update(defaultcfg, overwrite = False, protect_structure = True)

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
