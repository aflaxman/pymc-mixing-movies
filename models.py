""" Discussion on the PyMC mailing list indicates many people are
having trouble getting Adaptive Metropolis step methods to work.
Let's have a look at what's going on.
"""

import pylab as pl
import pymc as mc

# simple models for some uniformly distributed subsets of the plane
def diagonal():
    X = mc.Uniform('X', lower=-1., upper=1., value=[0., 0.])

    @mc.potential
    def near_diag(X=X):
        if abs(X[0] - X[1]) < .05:
            return 0
        else:
            return -pl.inf

    return mc.Model(vars())
