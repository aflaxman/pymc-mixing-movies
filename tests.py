""" Tests """

# matplotlib will open windows during testing unless you do the following
import matplotlib
matplotlib.use("AGG") 

import models
import graphics

class TestClass:
    def setUp(self):
        pass

    def test_diagonal_model(self):
        m1 = models.diagonal('Metropolis')
        assert hasattr(m1, 'X'), 'model should have stoch X as attribute'

    def test_visualize_step_i(self):
        step = 'Adaptive Metropolis'
        m1 = models.x_diagonal(step)
        graphics.visualize_single_step(m1, 5, 0., step)

    def test_hit_and_run_stepper(self):
        m1 = models.x_diagonal('Hit-and-Run', iters=5)


