import unittest
import sys
print(sys.path)
from src.DFBTA import DFBTA

class DFBTATests(unittest.TestCase):
    def testEmptyStates(self):
        self.assertRaises(ValueError, DFBTA, [], [], [], [])

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(DFBTATests)
    runner = unittest.TextTestRunner()
    result = runner.run(suite)
    print(result)