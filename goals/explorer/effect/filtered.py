import explorer

class EffectFilter(explorer.CellEffectExplorer):
    """ Filter out some effects to be added into a goal explorer mechanism.

        This is useful if for example some effects have special values, or you want
        to filter out the null effect.

        Goals are also filtered, but tentatively : if a goal in the forbidden values,
        a new goal is requested. The second one is not filtered.
    """

    def __init__(self, effectexplorer, filtered_values):
        """@param effectexplorer   the effect explorer instance from which we wish
                                   to filter goals
           @param filtered_values  the filtered values, as a list of hyperrectangle
        """
        self.effectexplorer = effectexplorer
        self.dim = len(effectexplorer.s_feats)
        self.s_feats = effectexplorer.s_feats
        self.filtered_values = tuple(filtered_values)

    @property
    def size(self):
        return self.effectexplorer.size

    def _in_filtered_values(self, val):
        return any(self._in_hyperrectangle(hyperrectangle, val) for hyperrectangle in self.filtered_values)

    def _in_hyperrectangle(self, hr, val):
        return all((hr_i_low <= v_i <= hr_i_high) for (hr_i_low, hr_i_high), v_i in zip(hr, val))

    def next_goal(self):
        """Generate a new goal"""
        goal = self.effectexplorer.next_goal()
        if self._in_filtered_values(goal):
            goal = self.effectexplorer.next_goal()
        return goal

    def add_effect(self, effect, goal = None):
        """Add an goal, and the actual effect obtained"""
        if not self._in_filtered_values(effect):
            self.effectexplorer.add_effect(effect, goal)

    def cell_list(self):
        """Return a list of region uid"""
        return self.explorer.cell_list()

    def active_cell_list(self):
        """Return a list of region uid"""
        return self.explorer.active_cell_list()

    def point2cell(self, point):
        """Return the region uid of the given effect"""
        return self.explorer.point2cell(point)