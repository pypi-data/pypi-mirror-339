
import unittest
import sys 
import os 

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from pymathisrtelib.functions import get_results, get_token

class TestGetResults(unittest.TestCase):
    def test_get_results(self):
        self.assertTrue(get_results("SELECT * FROM PUBLIC.CONVERGENCE.BILANPF LIMIT 100", get_token()))
        
if __name__=='__main__':
    unittest.main()
