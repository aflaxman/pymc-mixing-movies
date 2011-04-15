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
    mod.true_mean = [0,0]
    mod.true_iqr = ['(-.5,.5)', '(-.5,5)']
    return mod

def diagonal(step='Metropolis', iters=5000):
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

    mod = setup_and_sample(vars(), step, iters)
    mod.shape = pl.array([[-1,-1], [-1,-.9], [.9,1], [1,1], [1,.9], [-.9,-1], [-1,-1]])
    mod.true_mean = [0,0]
    mod.true_iqr = ['(-.5,.5)', '(-.5,5)']
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
    mod.true_mean = [0,0]
    mod.true_iqr = ['(-.5,.5)', '(-.5,5)']
    return mod

def banana(dim=2, b=.03, step='Metropolis', iters=5000):
    """ The non-linear banana-shaped distributions are constructed
    from the Gaussian ones by 'twisting' them as follows.  Let f be
    the density of the multivariate normal distribution N(0, C_1) with
    the covariance again given by C_1 = diag(100, 1, ..., 1).  The
    density function of the 'twisted' Gaussian with the nonlinearity
    parameter b > 0 is given by f_b = f \circ \phi_b, where the
    function \phi)b = (x_1, x_2 + b x_1^2 - 100b, x_3, ..., x_n).
    """
    assert dim >= 2, 'banana must be dimension >= 2'
    C_1 = pl.ones(dim)
    C_1[0] = 100.
    X = mc.Uninformative('X', value=pl.zeros(dim))

    def banana_like(X, tau, b):
        phi_X = pl.copy(X)
        phi_X *= 30. # rescale X to match scale of other models
        phi_X[1] = phi_X[1] + b*phi_X[0]**2 - 100*b

        return mc.normal_like(phi_X, 0., tau)

    @mc.potential
    def banana(X=X, tau=C_1**-1, b=b):
        return banana_like(X, tau, b)

    mod = setup_and_sample(vars(), step, iters)
    im = pl.imread('banana.png')
    x = pl.arange(-1, 1, .01)
    y = pl.arange(-1, 1, .01)
    z = [[banana_like(pl.array([xi, yi]), C_1[[0,1]]**-1, b) for xi in x] for yi in y]
    def plot_distribution():
        pl.imshow(im, extent=[-1,1,-1,1], aspect='auto', interpolation='bicubic')
        pl.contour(x, y, z, [-1000, -10, -6], cmap=pl.cm.Greys, alpha=.5)
    mod.plot_distribution = plot_distribution

    return mod


import steppers
reload(steppers)
import history_steps
reload(history_steps)

def setup_and_sample(vars, step, iters=5000):
    mod = mc.MCMC(vars)
    if step == 'AdaptiveMetropolis':
        mod.use_step_method(mc.AdaptiveMetropolis, mod.X)
    elif step == 'Hit-and-Run':
        mod.use_step_method(steppers.HitAndRun, mod.X, proposal_sd=.1)
    elif step == 'H-RAM':
        #mod.use_step_method(steppers.HRAM, mod.X, proposal_sd=.01)
        mod.use_step_method(history_steps.HRAM, mod.X, init_history=mc.rnormal(mod.X.value, 1., size=(20, len(mod.X.value))), xprime_sds=2, xprime_n=51)
    elif step == 'Metropolis':
        mod.use_step_method(mc.Metropolis, mod.X, proposal_sd=.1)
    else:
        raise Exception, 'Unrecognized Step Method'
    mod.sample(iters)

    return mod

def make_examples():
    for step in ['Hit-and-Run', 'AdaptiveMetropolis', 'Metropolis']:
        for model in [x_diagonal, diagonal, uniform]:
            print step, model.__name__
            m = model(step)
            graphics.visualize_steps(m, '%s_%s.avi' % (model.__name__, step[0]), step)

def make_bananas():
    for step in ['H-RAM', 'Hit-and-Run', 'AdaptiveMetropolis', 'Metropolis']:
        for b in [0., .03, .1]:
            for dim in [2, 4, 8]:
                print step, b, dim
                m = banana(b=b, dim=dim, step=step)
                graphics.visualize_steps(m, 'banana_b_%.2f_dim_%d_%s.avi' % (b, dim, step), step)

if __name__ == '__main__':
    make_examples()

    #graphics.visualize_single_step(m, 101, .5, 'Hit-and-Run')

