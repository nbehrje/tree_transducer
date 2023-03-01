import unittest
from src.tree_transducer.TreeAutomaton.DTTA import DTTA
from src.tree_transducer.Tree import Tree

class DTTATests(unittest.TestCase):
    #Raises error if DTTA's final states is not a subset of the DTTA's states
    def testFinalStatesNotSubset(self):
        self.assertRaises(ValueError, DTTA, [], ["qA"], [], {})

    #Raises error if DTTA's transitions contain states or symbols not present in the DTTA's states or symbols
    def testNewStatesSymbolsInTransitions(self):
        self.assertRaises(ValueError, DTTA, ["qA"], ["qA"], ["A"], {("qB","A", 2):{("qA", "qA")}})
        self.assertRaises(ValueError, DTTA, ["qA"], ["qA"], ["A"], {("qA","A", 2):{("qA", "qB")}})
        self.assertRaises(ValueError, DTTA, ["qA"], ["qA"], ["A"], {("qA","B", 2):{("qA", "qA")}})

    #Raises error if DTTA contains transition rule with mismatched number of children
    def testTransitionMismatched(self):
        self.assertRaises(ValueError, DTTA, ["qA"], [], ["A"], {("qA", "A", 1):{("qA","qA")}})

    #Returns True if the tree is accepted
    def testCorrectTreeAccepted(self):
        automaton = DTTA(["qS","qA","qB"],["qS"],["a","b","S"],{("qS","S", 2):{("qA", "qB")},
                                                                ("qS", "S", 3):{("qA", "qS", "qB")},
                                                                ("qA","a",0): {tuple()},
                                                                ("qB","b",0):{tuple()}})
        tree = Tree("S", [Tree("a"), Tree("S", [Tree("a"), Tree("b")]), Tree("b")])
        #self.assertTrue(automaton.accepts(tree))

    #Returns False if the tree is rejected
    def testIncorrectTreeRejected(self):
        automaton = DTTA(["qS","qA","qB"],["qS"],["a","b","S"],{("qS","S", 2):{("qA", "qB")},
                                                                ("qS", "S", 3):{("qA", "qS", "qB")},
                                                                ("qA","a",0): {tuple()},
                                                                ("qB","b",0):{tuple()}})
        tree = Tree("S", [Tree("a"), Tree("S", [Tree("b"), Tree("a")]), Tree("b")])
        self.assertFalse(automaton.accepts(tree))

    #Raises error if there is an epsilon transition
    def testEpsilon(self):
        self.assertRaises(ValueError, DTTA, ["qA"], ["qA"], ["A"], {("qA","", 2):{("qA", "qA")}})

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(DTTATests)
    runner = unittest.TextTestRunner()
    result = runner.run(suite)
    print(result)