import unittest
from src.tree_transducer.Tree import Tree

class TreeTests(unittest.TestCase):
    #Raises error if Tree has a None node with children
    def testTreeEmptyNode(self):
        self.assertRaises(ValueError, Tree, None, ["A"])

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TreeTests)
    runner = unittest.TextTestRunner()
    result = runner.run(suite)
    print(result)