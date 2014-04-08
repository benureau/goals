import forest

from ..tools.splittree import SplitTree
from cell import DualCell

defcfg = forest.Tree()

class CellTree(object):
    """Class instanciating cells around a SplitTree"""

    def __init__(self, bounds, crit_size, cfg, w = None):
        self.dim       = len(bounds)
        self.bounds    = bounds
        self.crit_size = crit_size
        self.w         = w
        if self.w is None:
            self.w = len(bounds)*[1.0]
        self.cfg       = cfg

        self.cellcount   = 0
        self.cells       = [DualCell(self.bounds, self, 0, self.cfg, w = self.w)]

        # keeping track of leaves and nodes
        self.leafcells = set([self.cells[0]])
        self.nodecells = set()

        # keeping track of node cells with effects
        self.active_cells = set()

        self.splittree = SplitTree(self.bounds, self.crit_size, div = 0,
                                   cell = self.cells[0])

    def __len__(self):
        return self.cellcount

    def add(self, effect, goal = None, prediction = None, competence = None, pred_error = None):
        """Add a point in the splittree"""
        self.splittree.add(effect)
        if goal is not None:
            self._add_goal(goal, effect, competence = competence)
        if prediction is not None or pred_error is not None:
            self._add_effect(effect, prediction, pred_error = pred_error)

    def _add_goal(self, goal, effect, competence = None):
        cells_uid = self.splittree.cells_of(goal)
        for idx in cells_uid:
            self.cells[idx].add(effect, goal = goal, competence = competence)

    def _add_effect(self, effect, prediction = None, pred_error = None):
        cells_uid = self.splittree.cells_of(effect)
        for idx in cells_uid:
            self.cells[idx].add(effect, prediction = prediction, pred_error = pred_error)

        if len(cells_uid) > 0:
            leafuid = cells_uid[0]
            if self.cells[leafuid].leaf and len(self.cells[leafuid].ecell) > 0:
                self.active_cells.add(self.cells[leafuid])

    def split(self, cell, low_cell, high_cell):
        self.cells.append(low_cell)
        self.cells.append(high_cell)
        low_cell.uid = self.cellcount
        high_cell.uid = self.cellcount + 1
        self.cellcount += 2
        self.leafcells.remove(cell)
        self.nodecells.add(cell)
        self.leafcells.add(low_cell)
        self.leafcells.add(high_cell)

        if len(cell.ecell) > 0:
            self.active_cells.remove(cell)
            if len(low_cell.ecell) > 0:
                self.active_cells.add(low_cell)
            if len(high_cell.ecell) > 0:
                self.active_cells.add(high_cell)


    def _belongs_to(self, point, bounds):
        return all(min_pi <= pi <= max_pi for pi, (min_pi, max_pi) in zip(point, bounds))

