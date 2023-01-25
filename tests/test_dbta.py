import unittest
from src.tree_transducer.TreeAutomaton.DBTA import DBTA
from src.tree_transducer.Tree import Tree

class DBTATests(unittest.TestCase):
    #Raises error if DBTA's final states is not a subset of the DBTA's states
    def testFinalStatesNotSubset(self):
        self.assertRaises(ValueError, DBTA, [], ["qA"], [], [])

    #Raises error if DBTA's transitions contain states or symbols not present in the DBTA's states or symbols
    def testNewStatesSymbolsInTransitions(self):
        self.assertRaises(ValueError, DBTA, ["qA"], [], ["A"], {(("qA",), "A"): "qA",(("qB",), "A"): "qA"})
        self.assertRaises(ValueError, DBTA, ["qA"], [], ["A"], {(("qA",), "A"): "qA",(("qA",), "B"): "qA"})

    #Returns True if the tree is accepted
    def testCorrectTreeAccepted(self):
        automaton = DBTA(["qA"],["qA"],["A"],{(("qA","qA"),"A"):"qA", (tuple(),"A"):"qA"})
        tree = Tree("A", [Tree("A"), Tree("A", [Tree("A"), Tree("A")])])
        self.assertTrue(automaton.accepts(tree))

    #Returns False if the tree is rejected
    def testIncorrectTreeRejected(self):
        automaton = DBTA(["qA"],["qA"],["A"],{(("qA","qA"),"A"):"qA", (tuple(),"A"):"qA"})
        tree = Tree("A", [Tree("A"), Tree("A", [Tree("A")])])
        self.assertFalse(automaton.accepts(tree))

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(DBTATests)
    runner = unittest.TextTestRunner()
    result = runner.run(suite)
    print(result)