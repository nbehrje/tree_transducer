import unittest
from src.DFBTA import DFBTA
from src.Tree import Tree

class DFBTATests(unittest.TestCase):
    #Raises error if DFBTA's final states is not a subset of the DFBTA's states
    def testFinalStatesNotSubset(self):
        self.assertRaises(ValueError, DFBTA, [], ["qA"], [], [])

    #Raises error if DFBTA's transitions contain states or symbols not present in the DFBTA's states or symbols
    def testNewStatesSymbolsInTransitions(self):
        self.assertRaises(ValueError, DFBTA, ["qA"], [], ["A"], {(("qA",), "A"): "qA",(("qB",), "A"): "qA"})
        self.assertRaises(ValueError, DFBTA, ["qA"], [], ["A"], {(("qA",), "A"): "qA",(("qA",), "B"): "qA"})

    #Returns True if the tree is accepted
    def testCorrectTreeAccepted(self):
        automaton = DFBTA(["qA"],["qA"],["A"],{(("qA","qA"),"A"):"qA", (tuple(),"A"):"qA"})
        tree = Tree("A", [Tree("A"), Tree("A", [Tree("A"), Tree("A")])])
        self.assertTrue(automaton.accepts(tree))

    #Returns False if the tree is accepted
    def testIncorrectTreeRejected(self):
        automaton = DFBTA(["qA"],["qA"],["A"],{(("qA","qA"),"A"):"qA", (tuple(),"A"):"qA"})
        tree = Tree("A", [Tree("A"), Tree("A", [Tree("A")])])
        self.assertFalse(automaton.accepts(tree))

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(DFBTATests)
    runner = unittest.TextTestRunner()
    result = runner.run(suite)
    print(result)