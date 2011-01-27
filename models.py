""" Discussion on the PyMC mailing list indicates many people are
having trouble getting Adaptive Metropolis step methods to work.
Let's have a look at what's going on.
"""

import pylab as pl
import pymc as mc
import graphics

inf = pl.inf

# simple models for some uniformly distributed subsets of the plane
def uniform(step):
    X = mc.Uniform('X', lower=-1., upper=1., value=[0., 0.])
    return setup_and_sample(vars(), step)

def diagonal(step):
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

    return setup_and_sample(vars(), step)

def x_diagonal(step, iters=5000):
    X = mc.Uniform('X', lower=-1., upper=1., value=[0., 0.])

    @mc.potential
    def near_x_diags(X=X):
        if abs(X[0] - X[1]) < .1:
            return 0
        elif abs(X[0] + X[1]) < .1:
            return 0
        else:
            return -inf

    return setup_and_sample(vars(), step, iters)


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

def make_uniform_examples():
    m = mc.MCMC({'X': mc.Uniform('X', lower=-1, upper=1, value=[0,0])})
    m.use_step_method(mc.Metropolis, m.X)
    m.sample(3000)
    graphics.visualize_steps(m, 'uniform_M.avi')

    m = mc.MCMC({'X': mc.Uniform('X', lower=-1, upper=1, value=[0,0])})
    m.use_step_method(mc.AdaptiveMetropolis, m.X)
    m.sample(3000)
    graphics.visualize_steps(m, 'uniform_AM.avi')

def make_examples():
    for step in ['Hit-and-Run', 'Adaptive Metropolis', 'Metropolis']:
        for model in [x_diagonal, diagonal]:
            print step, model.__name__
            m = model(step)
            graphics.visualize_steps(m, '%s_%s.avi' % (model.__name__, step[0]), step)

if __name__ == '__main__':
    m = x_diagonal('Hit-and-Run', 200)
    reload(graphics)
    graphics.visualize_single_step(m, 101, .5, 'Hit-and-Run')
    pl.show()
