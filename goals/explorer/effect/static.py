"""Static goal explorer are bounded goal explorer which have the partition of
the goal space manually defined, and unchanging. They are very useful to test
different hypothesis.

A possible setup is to use a random explorer to decide the next random goal,
and multiple static explorer to analyse how the rates the interestingness of
the space, depending on the partition.
"""
import treedict

import toolbox

from explorer import CellEffectExplorer
from cell import DualCell

defaultcfg = treedict.TreeDict()

defaultcfg.s_areas = None
defaultcfg.s_areas = "the list of areas to consider when tracking interest"

class StaticExplorer(CellEffectExplorer):

    def __init__(self, s_feats, cfg):
        """
        :param  s_areas  a list of hyperrectangles (same format as s_bounds).
                        they don't need to cover the space entirely, and they
                        can overlap. When an observation falls in a region,
                        it will be updated independently of all other.
                        There is no notion of neighborhood in this class.
        """
        self.dim = len(s_feats)
        self.s_feats = tuple(s_feats)

        if cfg.get('s_areas', None) is None:
            print "You must define the s_areas config parameter for GridExplorer"
        self.cells = [DualCell(bounds, self, uid, depth = 0, w = None, cfg = cfg) for uid, bounds in enumerate(cfg.s_areas)]

        self.active_cells = set()

    def add_effect(self, effect, goal = None, prediction = None):
        for cell in self.cells:
            active = cell.add(effect, goal = goal, prediction = prediction)
            if active:
                self.active_cells.add(cell)

    def next_goal(self):
        # choose an area proportionally to its interest
        index = toolbox.roulette_wheel([cell.interest() for cell in self.cells])
        # choose a random goal in it.
        goal = self.cells[index].random_point()
        return goal

    def point2cell(self, point): # TODO: return list of cells !
        for cell in self.cells:
            if cell.belongs(point):
                return cell