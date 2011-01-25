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
        m1 = models.diagonal()
        assert hasattr(m1, 'X'), 'model should have stoch X as attribute'

    def test_visualize_step_i(self):
        m1 = models.diagonal()
        m1.sample(10)

        graphics.visualize_steps(m1.X, 5)

