import numpy as np
import toolbox

class Meshgrid(object):
    
    def __init__(self, dim, res, sigma):
        assert dim <= 3
        self.dim   = dim
        self.res   = res
        self.sigma = sigma
        self.nhood = max(1, int(2*sigma/res))
        self.nodes = {}
        self.size  = 0
        
    def _nhood(self, p):
        p_center = np.array([int(p[i]/self.res) for i in range(self.dim)])
        nhood = []
        if self.dim == 2:
            cx, cy = p_center
            for i in range(-self.nhood, self.nhood +1):
                for j in range(-self.nhood, self.nhood +1):
                    nhood.append((cx + i, cy + j))
        if self.dim == 3:
            cx, cy, cz = p_center
            for i in range(-self.nhood, self.nhood +1):
                for j in range(-self.nhood, self.nhood +1):
                    for k in range(-self.nhood, self.nhood +1):
                        nhood.append((cx + i, cy + j, cz + k))
        return nhood, p_center

    def __len__(self):
        return self.size

    def add_p(self, p, v):
        self.size += 1
        nhood, center = self._nhood(p)
        for n_p in nhood:
            d = toolbox.dist(p, self.res*np.array(n_p))
            w = toolbox.gaussian_kernel(d, self.sigma*self.sigma)
            #print w
            self.nodes[n_p] = self.nodes.get(n_p, 0.0)*(1-w) + w*v

    def _MN(self, extent):
        """Return a meshgrid ready for display"""
        assert self.dim == 2
        xmin, xmax, ymin, ymax = extent
        width  = (xmax-xmin)/self.res
        height = (ymax-ymin)/self.res
        heatmap = np.zeros((width, height))
        for i in range(width):
            for j in range(height):
                heatmap[i][j] = np.nan
        for n_p, inte in self.nodes.iteritems():
            x, y = n_p
            try: 
                heatmap[-y+int(ymin/self.res)][x-int(xmin/self.res)] = inte
            except IndexError:
                pass
        return heatmap

    def _meshgrid(self, res = None):
        """Return a meshgrid of resolution res."""

        res = res or self.res
        heatmap   = np.zeros((res+2*margin, res+2*margin))
        weightmap = np.zeros((res+2*margin, res+2*margin))

#        print list(self.self.dataset.iter_x())
        if self.extent is not None:
            xmin, xmax, ymin, ymax = self.extent
            bounds0 = xmin, xmax
            bounds1 = ymin, ymax
        else:
            bounds0 = min((y[0] for y in self.dataset.iter_x())), max((y[0] for y in self.dataset.iter_x()))
            bounds1 = min((y[1] for y in self.dataset.iter_x())), max((y[1] for y in self.dataset.iter_x()))

        for y, c in self.dataset.iter_xy():
            center = (margin - 1 + (y[0]-bounds0[0])/(max(1.0, bounds0[1]-bounds0[0]))*res, 
                      margin - 1 + (y[1]-bounds1[0])/(max(1.0, bounds1[1]-bounds1[0]))*res)
            neighborhood = []
            for i in range(-4, 5):
                for j in range(-4, 5):
                    neighborhood.append((int(center[0])+i, int(center[1])+j))
            for ng in neighborhood:
                d = toolbox.dist(ng, center)
                w = math.exp(-d*d/4)
                heatmap[-ng[1]][ng[0]]   += w*c
                weightmap[-ng[1]][ng[0]] += w

        for i in range(res+2*margin):
            for j in range(res+2*margin):
                w = weightmap[i][j]
                if w > 0:
                    heatmap[i][j] /= 1+w

        return heatmap, (bounds0, bounds1)    