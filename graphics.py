""" put messy matplotlib code here so I don't have to look at it if I
don't want to
"""

import pylab as pl
import sys

def visualize_single_step(mod, i, alpha=0., description_str=''):
    """ Show how a random walk in a two dimensional space has
    progressed up to step i"""

    X = mod.X.trace()

    pl.clf()

    sq_size=.3

    # show 2d trace
    pl.axes([.05, .05, sq_size, sq_size])

    pl.plot(X[:i, 0], X[:i, 1], 'b.-', alpha=.1)

    Y = alpha * X[i, :] + (1 - alpha) *X[i-1, :]
    pl.plot([Y[0], Y[0]], [Y[1], 2.], 'k-', alpha=.5)
    pl.plot([Y[0], 2], [Y[1], Y[1]], 'k-', alpha=.5)
    pl.plot(Y[0], Y[1], 'go')

    if hasattr(mod, 'shape'):
        pl.fill(mod.shape[:,0], mod.shape[:,1], color='b', alpha=.2)
    if hasattr(mod, 'plot_distribution'):
        mod.plot_distribution()

    pl.axis([-1.1, 1.1, -1.1, 1.1])
    pl.xticks([])
    pl.yticks([])

    # show 1d marginals

    ## X[0] is horizontal position
    pl.axes([.05, .05+sq_size, sq_size, 1.-.1-sq_size])
    pl.plot(X[:(i+1), 0], i+1-pl.arange(i+1), 'k-')
    pl.axis([-1.1, 1.1, 0, 1000])
    pl.xticks([])
    pl.yticks([])
    pl.text(-1, .1, '$X_0$')

    ## X[1] is vertical position
    pl.axes([.05+sq_size, .05, 1.-.1-sq_size, sq_size])
    pl.plot(i+1-pl.arange(i+1), X[:(i+1), 1], 'k-')
    pl.axis([0, 1000, -1.1, 1.1])
    pl.xticks([])
    pl.yticks([])
    pl.text(10, -1., '$X_1$')

    ## show X[i, j] acorr
    N, D = X.shape
    if i > 250:
        for j in range(D):
            pl.axes([1-.1-1.5*sq_size*(1-j*D**-1.), 1.-.1-1.5*sq_size*D**-1, 1.5*sq_size*D**-1., 1.5*sq_size*D**-1.])
            pl.acorr(X[(i/2):i:10, j], detrend=pl.mlab.detrend_mean)
            pl.xlabel('$X_%d$'%j)
            if j == 0:
                pl.ylabel('autocorr')
            pl.xticks([])
            pl.yticks([])
            pl.axis([-10, 10, -.1, 1])
    ## show X[1] acorr

    ## textual information
    str = ''
    str += 't = %d\n' % i
    str += 'acceptance rate = %.2f\n\n' % (1. - pl.mean(pl.diff(X[:i, 0]) == 0.))

    str += 'mean(X) = %s' % pretty_array(X[:i, :].mean(0))
    if hasattr(mod, 'true_mean'):
        str += ' / true mean = %s\n' % pretty_array(mod.true_mean)
    else:
        str += '\n'

    if i > 0:
        iqr = pl.sort(X[:i,:], axis=0)[[.25*i, .75*i], :].T

        for j in range(D):
            str += 'IQR(X[%d]) = (%.2f, %.2f)' % (j, iqr[j,0], iqr[j,1])
            if hasattr(mod, 'true_iqr'):
                str += ' / true IQR = %s\n' % mod.true_iqr[j]
            else:
                str += '\n'
    pl.figtext(.05 + .01 + sq_size, .05 + .01 + sq_size, str, va='bottom', ha='left')

    pl.figtext(sq_size + .5 * (1. - sq_size), .9, 
               description_str, va='top', ha='center', size=32)

    pl.figtext(.95, .05, 'healthyalgorithms.wordpress.com', ha='right')

def visualize_steps(mod, fname='mod.avi', description_str=''):
    times = list(pl.arange(0, 30, .2)) + range(30, 200) + range(200, 1500, 10)
    times += range(1500, 1700) + range(1700, 3000, 10)
    times += range(3000, 3200) + range(3200, len(mod.X.trace()), 10)
    assert pl.all(pl.diff(times) >= 0.), 'movies where time is not increasing are confusing and probably unintentional'
    try:
        print 'generating %d images' % len(times)
        for i, t in enumerate(times):
            if i % 100 == 99:
                print '%d of %d (t=%.2f)' % (i, len(times), t)
            sys.stdout.flush()
            visualize_single_step(mod, int(t), t - int(t), description_str)
            pl.savefig('mod%06d.png' % i)
    except KeyboardInterrupt:
        pass

    import subprocess
    subprocess.call('mencoder mf://mod*.png -mf w=800:h=600 -ovc x264 -of avi -o %s' % fname, shell=True)
    subprocess.call('mplayer -loop 1 %s' % fname, shell=True)
    subprocess.call('rm mod*.png', shell=True)

def pretty_array(x):
    return '(%s)' % ', '.join('%.2f' % x_i for x_i in x)
