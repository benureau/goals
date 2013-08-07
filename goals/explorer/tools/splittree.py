
import random

class SplitTree(object):
    """ A pure data structure class, keeps datapoints in a multidimensional quadtree.

        Only spatial coordinates are relevant.
        Splits are made when the size of a regions exceeds a given limit.
        Only necessary splits are made (no splitting of empty regions).
        The split is made a the middle of the region.
        A split can trigger another if all points are on one side of the cutoff value.
        Dimensions are splitted one after the other, in circular order.
    """

    def __init__(self, bounds, crit_size, div = 0, min_size = None, cell = None):
        """Creates a splittree.

            :arg  bounds:          (min, max) values for each dimension.
                                   this also implicitely indicate the dimension of the tree.
            :type bounds:          iterable of pairs of floats.
            :arg  crit_size:       the maximum size of a region. Exceeding this, a split
                                   is triggered.
            :arg  div:             the starting dimension for a split.
            :arg  cell:            a DualCell instance linked to this node of the splittree.
        """
        self.bounds = tuple(bounds)
        self.crit_size = crit_size

        self.min_size = min_size
        if self.min_size is None:
            self.min_size = tuple((max_i - min_i)/64.0 for min_i, max_i in self.bounds)
        self.div    = self._divisible_dim(div) # along which dim the split is (and can be) made
                                               # if None, cell is atomic: can't be splitted anymore
        self.cutoff = None   # what it the value of the split

        self.datapoints = []
        self.leaf     = True   # False if children exist

        self.children = [None, None]

        self.cell = cell

    def add(self, datapoint):
        if self.leaf and self.div is not None and len(self.datapoints) >= self.crit_size:
            self._split()
        self.datapoints.append(datapoint)

        if not self.leaf:
            child = self._belongs_to(datapoint)
            child.add(datapoint)

    def _divisible_dim(self, div):
        """Find the next div along which the tree can be divided, starting with div"""
        n = len(self.bounds)
        for i in range(n):
            j = (i+div) % n
            min_j, max_j = self.bounds[j]
            if (max_j - min_j) / 2.0 >= self.min_size[j]:
                return j
        return None

    def _split(self):
        self.cutoff = (self.bounds[self.div][1] + self.bounds[self.div][0])/2.0

        low_bounds = list(self.bounds)
        low_bounds[self.div] = (self.bounds[self.div][0], self.cutoff)

        high_bounds = list(self.bounds)
        high_bounds[self.div] = (self.cutoff, self.bounds[self.div][1])

        low_cell, high_cell = None, None
        if self.cell is not None:
            self.cell.split(low_bounds, high_bounds)

        # Split gcells before ecells, it's important !
        self.children[0] = SplitTree(low_bounds, self.crit_size,
                                     div = (self.div+1) % len(self.bounds),
                                     min_size = self.min_size,
                                     cell = low_cell)

        self.children[1] = SplitTree(high_bounds, self.crit_size,
                                     div = (self.div+1) % len(self.bounds),
                                     min_size = self.min_size,
                                     cell = high_cell)

        self.children = tuple(self.children)

        for dp in self.datapoints:
            child = self._belongs_to(dp)
            child.add(dp)

        self.leaf = False

    def _belongs_to(self, dp):
        if dp[self.div] <= self.cutoff:
            return self.children[0]
        else:
            return self.children[1]

    def cells_of(self, dp):
        """Return a list of the uid of the gcells which contain dp"""
        if self.leaf:
            if self.cell is None:
                return []
            else:
                return [self.cell.uid]
        else:
            uids = self._belongs_to(dp).cells_of(dp)
            if self.cell is not None:
                uids.append(self.cell.uid)
            return uids

    def leaf_of(self, dp):
        if self.leaf:
            if self.cell is not None:
                return self.cell
        else:
            return self._belongs_to(dp).leaf_of(dp)
