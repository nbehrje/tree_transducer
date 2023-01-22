import unittest
from src.Tree import Tree

class TreeTests(unittest.TestCase):
    #Raises error if Tree has a None node with children
    def testTreeEmptyNode(self):
        self.assertRaises(ValueError, Tree, None, ["A"])