""" Discussion on the PyMC mailing list indicates many people are
having trouble getting Adaptive Metropolis step methods to work.
Let's have a look at what's going on.
"""

import pylab as pl
import pymc as mc

# simple models for some uniformly distributed subsets of the plane
