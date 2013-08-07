import random

from pubsub import pub
import treedict

import toolbox
from toolbox import gfx

import explorer
import cell

defaultcfg = treedict.TreeDict()

defaultcfg.effect.s_res = 10
defaultcfg.effect.s_res_desc = "Number of row for each feature in the grid."

defaultcfg.effect.random_explo = 0.05
defaultcfg.effect.random_explo_desc = "Percentage of random exploration"

defaultcfg.effect.unknown_explo = 0.10
defaultcfg.effect.unknown_explo_desc = "Percentage of unknown areas exploration"

defaultcfg.effect.sample_size = 3
defaultcfg.effect.sample_size_desc = "how many goal to pick per region at minimum regardless of the interest measure"

defaultcfg.effect.s_bounds = None
defaultcfg.effect.s_bounds_desc = "the limit of the sensory features"


class GridExplorer(explorer.CellEffectExplorer):
    """"""

    @classmethod
    def from_robot(cls, robot, cfg, cellclass = cell.DualCell):
        """Convenience function if the robot support s_bounds and s_res"""
        return cls(robot.s_feats, cfg, cellclass = cellclass)

    def __init__(self, s_feats, cfg, cellclass = cell.DualCell):
        """ Initilization

            :param s_feats:   the sensory features
            :type  s_feats:   tuple of ints
            :param s_bounds:  bounds for each sensory features
            :type  s_bounds:  tuple of length 2 tuples of floats
            :param s_res:     how many cell to create for each dimension
            :type  s_res:     tuple of ints
        """
        self.dim = len(s_feats)
        self.s_feats = s_feats

        assert cfg.effect.get('s_bounds', None) != None, "{}you must define the s_bounds parameter for GridExplorer{}".format(gfx.red, gfx.end)
        assert len(cfg.effect.s_bounds) == self.dim
        self.bounds = cfg.effect.s_bounds

        self.cfg = cfg
        self.cfg.update(defaultcfg, overwrite = False)

        if type(cfg.effect.s_res) == int:
            self.s_res = [cfg.effect.s_res]*self.dim
        else:
            assert len(cfg.effect.s_res) == self.dim
            self.s_res = cfg.effect.s_res

        self.size = 0
        pub.sendMessage('grid.init', grid = self, size = self.s_res, bounds = self.bounds)
        self.grid = {}
        self.cells = [] # list of cells for random choice
        self.active_cells = set()
        self.cellclass = cellclass
        self._build_grid()

    def _build_grid(self, prefix = []):
        lenp = len(prefix)
        if lenp == self.dim:
            coo = tuple(prefix)
            bounds_p = [(float(pi)/res_i*(si_max-si_min) + si_min, float(pi+1)/res_i*(si_max-si_min) + si_min)
                         for pi, res_i, (si_min, si_max) in
                         zip(prefix, self.s_res, self.bounds)]
            self.grid[coo] = self.cellclass (bounds_p, self, coo, self.cfg, depth = 0, w = self.s_res)
            self.cells.append(self.grid[coo])
        else:
            for i in range(self.s_res[lenp]):
                self._build_grid(prefix = prefix + [i])

    def _coo(self, p):
        """ Return the coordinate of the cell where p belongs """
        assert len(p) == self.dim
        coo = []
        for pi, (si_min, si_max), res_i in zip(p, self.bounds, self.s_res):
            assert si_min <= pi <= si_max, "effect {} is not within the boundaries {}".format(p, self.bounds)
            coo.append(min(res_i-1, int((pi-si_min)/(si_max-si_min)*res_i)))
        return tuple(coo)

    def point2cell(self, p):
        return self.grid[self._coo(p)]

    def _nhood(self, coo):
        """ Return the list of adjacent cells of a cell """
        nhood = []
        for i in range(self.dim):
            nbor_low  = list(coo)
            nbor_low[i]  -= 1
            nbor_low = tuple(nbor_low)
            if nbor_low in self.grid:
                nhood.append(self.grid[nbor_low])
            nbor_high = list(coo)
            nbor_high[i] += 1
            nbor_high = tuple(nbor_high)
            if nbor_high in self.grid:
                nhood.append(self.grid[nbor_high])
        return nhood

    def add_effect(self, effect, goal = None, prediction = None):
        """ Add an goal, and the actual effect obtained """
        self.size += 1
        coo = self._coo(effect)
        self.grid[coo].add_effect(effect, prediction = prediction)
        self.active_cells.add(self.grid[coo])
        if goal is not None:
            coo = self._coo(goal)
            self.grid[coo].add_goal(effect, goal)

        # pub.sendMessage('grid.competence_update', grid=self, coo=coo, competence=c)
        # pub.sendMessage('grid.interest_update', grid=self, coo=coo, interest=self.grid[coo].interests[-1])

    def next_goal(self):
        """Generate a new goal"""
        # decide between trying a virgin available cell
        # or an interesting cell
        dice = random.random()
        if dice < self.cfg.effect.random_explo:
            idx = random.randint(0, len(self.cells) - 1)
        # elif dice < self.cfg.random_explo + self.cfg.unknown_explo:
        #     explo_interest = [cell.exploration_interest() for cell in self.cells]
        #     if sum(explo_interest) > 0:
        #         idx = toolbox.roulette_wheel(explo_interest)
        #     else:
        #         idx = toolbox.roulette_wheel([cell.interests[-1] for cell in self.cells])
        else:
            idx = toolbox.roulette_wheel([cell.interest() for cell in self.cells])

        return self.cells[idx].random_point()
