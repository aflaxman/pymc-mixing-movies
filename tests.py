""" Tests """

# matplotlib will open windows during testing unless you do the following
import matplotlib
matplotlib.use("AGG") 

import models

class TestClass:
    def setUp(self):
        pass

    def test_models(self):
        m1 = models.diagonal()
        assert hasattr(m1, 'X'), 'model should have stoch X as attribute'

