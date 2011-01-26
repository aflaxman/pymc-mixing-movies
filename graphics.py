import pylab as pl

# put messy matplotlib code here so I don't have to look at it if I
# don't want to

def visualize_single_step(mod, i, alpha):
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

    ## show X[0] acorr
    if i > 100:
        pl.axes([.05+.01, 1.-.1-sq_size*.5, sq_size*.5, sq_size*.5])
        pl.axis('off')
        pl.acorr(X[:i, 0], detrend=pl.mlab.detrend_mean)

    ## X[1] is vertical position
    pl.axes([.05+sq_size, .05, 1.-.1-sq_size, sq_size])
    pl.plot(i+1-pl.arange(i+1), X[:(i+1), 1], 'k-')
    pl.axis([0, 1000, -1.1, 1.1])
    pl.xticks([])
    pl.yticks([])
    pl.text(.1, -1., '$X_1$')

    ## show X[1] acorr
    if i > 100:
        pl.axes([1.-.1-sq_size*.5, .05+.01, sq_size*.5, sq_size*.5])
        pl.axis('off')
        pl.acorr(X[:i, 1], detrend=pl.mlab.detrend_mean)
    
    ## textual information
    str = ''
    str += 't = %d\n' % i
    #str += 'effective samples of X[0] = %.2f\n' % 0.
    #str += 'effective samples of X[1] = %.2f\n' % 0.
    str += 'mean(X) = (%.2f, %.2f)\n' % tuple(X[:i, :].mean(0))

    if i > 0:
        iqr = pl.sort(X[:i,:], axis=1)[[.025*i, .975*i], :].T
    else:
        iqr = pl.nan * pl.ones([2,2])
    str += 'IQR(X[0]) = (%.2f, %.2f)\n' % tuple(iqr[0,:])
    str += 'IQR(X[1]) = (%.2f, %.2f)\n' % tuple(iqr[1,:])
    pl.figtext(.05 + .01 + sq_size, .05 + .01 + sq_size, str, va='bottom', ha='left')

def visualize_steps(mod, fname='mod.avi'):
    times = list(pl.arange(0, 30, .2)) + range(20, 200) + range(200, len(mod.X.trace()), 10)
    print 'generating %d images' % len(times)
    for t in times:
        visualize_single_step(mod, int(t), t - int(t))
        pl.savefig('mod%06d.png' % int(t*100))

    import subprocess
    subprocess.call('mencoder mf://mod*.png -mf w=800:h=600 -ovc x264 -of avi -o %s' % fname, shell=True)
    subprocess.call('mplayer -loop 0 %s' % fname, shell=True)
    subprocess.call('rm mod*.png', shell=True)
