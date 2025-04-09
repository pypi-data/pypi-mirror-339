
import unittest
import sys 
import os 

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from pymathisrtelib.functions import get_nni

class TestGetNNI(unittest.TestCase):
    def test_get_nni(self):
        self.assertTrue(get_nni())
        
if __name__=='__main__':
    unittest.main()


