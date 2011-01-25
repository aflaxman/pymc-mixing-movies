""" Tests """

# matplotlib will open windows during testing unless you do the following
import matplotlib
matplotlib.use("AGG") 

import models

class TestClass:
   def setUp(self):
      pass

   def test_models(self):
       assert False, 'Write test, fail, write code, pass'
