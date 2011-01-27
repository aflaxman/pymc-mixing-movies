""" Discussion on the PyMC mailing list indicates many people are
having trouble getting Adaptive Metropolis step methods to work.
Let's have a look at what's going on.
"""

import pylab as pl
import pymc as mc
import graphics
reload(graphics)

inf = pl.inf

# simple models for some uniformly distributed subsets of the plane
def uniform(step='Metropolis', iters=5000):
    X = mc.Uniform('X', lower=-1, upper=1, value=[0,0])
    mod = setup_and_sample(vars(), step, iters)
    mod.shape = pl.array([[-1,-1], [-1,1], [1,1], [1,-1]])
    return mod

def diagonal(step='Metropolis'):
    """ create model for diagonal subset

    step : str, one of 'Adaptive Metropolis', 'Metropolis', 'Hit-and-Run'
        
    """
    X = mc.Uniform('X', lower=-1., upper=1., value=[0., 0.])

    @mc.potential
    def near_diag(X=X):
        if abs(X[0] - X[1]) < .1:
            return 0
        else:
            return -inf

    mod = setup_and_sample(vars(), step)
    mod.shape = pl.array([[-1,-1], [-1,-.9], [.9,1], [1,1], [1,.9], [-.9,-1], [-1,-1]])
    return mod

def x_diagonal(step='Metropolis', iters=5000):
    X = mc.Uniform('X', lower=-1., upper=1., value=[0., 0.])

    @mc.potential
    def near_x_diags(X=X):
        if abs(X[0] - X[1]) < .1:
            return 0
        elif abs(X[0] + X[1]) < .1:
            return 0
        else:
            return -inf

    mod = setup_and_sample(vars(), step, iters)
    mod.shape = pl.array([[-1,-1], [-1,-.9], [-.1,  0], [ -1, .9],
                          [-1, 1], [-.9, 1], [  0, .1], [ .9, 1],
                          [ 1, 1], [ 1, .9], [ .1,  0], [  1,-.9],
                          [ 1,-1], [.9, -1], [  0,-.1], [-.9,-1]])
    return mod


def setup_and_sample(vars, step, iters=5000):
    mod = mc.MCMC(vars)
    if step == 'Adaptive Metropolis':
        mod.use_step_method(mc.AdaptiveMetropolis, mod.X)
    elif step == 'Hit-and-Run':
        import steppers
        reload(steppers)
        mod.use_step_method(steppers.HitAndRun, mod.X, proposal_sd=.1)
    elif step == 'Metropolis':
        mod.use_step_method(mc.Metropolis, mod.X)
    else:
        raise Exception, 'Unrecognized Step Method'
    mod.sample(iters)

    return mod

def make_examples():
    for step in ['Hit-and-Run', 'Adaptive Metropolis', 'Metropolis']:
        for model in [x_diagonal, diagonal, uniform]:
            print step, model.__name__
            m = model(step)
            graphics.visualize_steps(m, '%s_%s.avi' % (model.__name__, step[0]), step)

if __name__ == '__main__':
    make_examples()

    #graphics.visualize_single_step(m, 101, .5, 'Hit-and-Run')

