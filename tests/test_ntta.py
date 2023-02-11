import unittest
from src.tree_transducer.TreeAutomaton.NTTA import NTTA
from src.tree_transducer.Tree import Tree

class NTTATests(unittest.TestCase):
    #Raises error if NBTA's final states is not a subset of the NBTA's states
    def testFinalStatesNotSubset(self):
        self.assertRaises(ValueError, NTTA, [], ["qA"], [], {})

    #Raises error if NTTA's transitions contain states or symbols not present in the NTTA's states or symbols
    def testNewStatesSymbolsInTransitions(self):
        self.assertRaises(ValueError, NTTA, ["qA"], ["qA"], ["A"], {("qB","A", 2):{("qA", "qA")}})
        self.assertRaises(ValueError, NTTA, ["qA"], ["qA"], ["A"], {("qA","A", 2):{("qA", "qB")}})
        self.assertRaises(ValueError, NTTA, ["qA"], ["qA"], ["A"], {("qA","B", 2):{("qA", "qA")}})
        self.assertRaises(ValueError, NTTA, ["qA"], ["qA"], ["A"], {("qA","A", 2):{("qA", "qA"),("qA", "qB")}})

    #Raises error if DTTA contains transition rule with mismatched number of children
    def testTransitionMismatched(self):
        self.assertRaises(ValueError, NTTA, ["qA"], [], ["A"], {("qA", "A", 1):{("qA","qA")}})
        self.assertRaises(ValueError, NTTA, ["qA"], [], ["A"], {("qA", "A", 1):{("qA"), ("qA","qA")}})

    #Returns True if the tree is accepted
    def testCorrectTreeAccepted(self):
        automaton = NTTA(["qS","qA","qB"],["qS"],["a","b","S"],{("qS","S", 2):{("qA", "qB")},
                                                                ("qS", "S", 3):{("qA", "qS", "qB")},
                                                                ("qA","a",0): {tuple()},
                                                                ("qB","b",0):{tuple()}})
        tree = Tree("S", [Tree("a"), Tree("S", [Tree("a"), Tree("b")]), Tree("b")])
        self.assertTrue(automaton.accepts(tree))
        automaton = NTTA(["qS","qA","qB"],["qS"],["a","b","S"],{("qS","S", 2):{("qA", "qB"), ("qA", "qA")},
                                                                ("qS", "S", 3):{("qA", "qS", "qB")},
                                                                ("qA","a",0): {tuple()},
                                                                ("qB","b",0):{tuple()}})
        tree = Tree("S", [Tree("a"), Tree("S", [Tree("a"), Tree("a")]), Tree("b")])
        self.assertTrue(automaton.accepts(tree))
        automaton = NTTA(["qS","qA","qB"],["qS"],["a","b","S"],{("qS","S", 2):{("qA", "qB"), ("qA", "qA")},
                                                                ("qS", "S", 3):{("qA", "qS", "qB")},
                                                                ("qA","a",0): {tuple()},
                                                                ("qB","b",0):{tuple()}})
        tree = Tree("S", [Tree("a"), Tree("S", [Tree("a"), Tree("a")]), Tree("b")])
        self.assertTrue(automaton.accepts(tree))