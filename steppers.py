""" Class to hold the model variables and do some fitting"""

from numpy import *
from pymc import *

class HitAndRun(Gibbs):
    def __init__(self, stochastic, proposal_sd=None, verbose=None):
        Metropolis.__init__(self, stochastic, proposal_sd=proposal_sd,
                            verbose=verbose, tally=False)
        self.proposal_tau = self.proposal_sd**-2.
        
    def step(self):
        x0 = copy(self.stochastic.value)
        dx = rnormal(zeros(len(x0)), self.proposal_tau)

        logp = [self.logp_plus_loglike]
        x_prime = [x0]

        for direction in [-1, 1]:
            for i in xrange(25):
                delta = direction*exp(.1*i)*dx
                try:
                    self.stochastic.value = x0 + delta
                    logp.append(self.logp_plus_loglike)
                    x_prime.append(x0 + delta)
                except ZeroProbability:
                    self.stochastic.value = x0
        
        i = rcategorical(exp(array(logp) - flib.logsum(logp)))
        self.stochastic.value = x_prime[i]

        if i == 0:
            self.rejected += 1
        else:
            self.accepted += 1
