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
        automaton = NTTA(["qS","qA","qB","qT","qR"],["qT"],["a","b","S"],{("qS","S", 2):{("qA", "qB"), ("qA", "qA")},
                                                                ("qS","S", 3):{("qA", "qS", "qB")},
                                                                ("qA","a",0): {tuple()},
                                                                ("qB","b",0):{tuple()},
                                                                ("qT","",1):{("qR",)},
                                                                ("qR","",1):{("qS",)}})
        tree = Tree("S", [Tree("a"), Tree("S", [Tree("a"), Tree("a")]), Tree("b")])
        self.assertTrue(automaton.accepts(tree))

    #Returns False if the tree is rejected
    def testIncorrectTreeRejected(self):
        automaton = NTTA(["qS","qA","qB","qT","qR"],["qT"],["a","b","S"],{("qS","S", 2):{("qA", "qB"), ("qA", "qA")},
                                                                ("qS","S", 3):{("qA", "qS", "qB")},
                                                                ("qA","a",0): {tuple()},
                                                                ("qB","b",0):{tuple()},
                                                                ("qT","",1):{("qR",)}})
        tree = Tree("S", [Tree("a"), Tree("S", [Tree("a"), Tree("a")]), Tree("b")])
        self.assertFalse(automaton.accepts(tree))

    #Returns epsilon closure
    def testEpsilonClosure(self):
        automaton = NTTA(["qS","qA","qB","qT","qR"],["qT"],["a","b","S"],{("qS","S", 2):{("qA", "qB"), ("qA", "qA")},
                                                                ("qS","S", 3):{("qA", "qS", "qB")},
                                                                ("qA","a",0): {tuple()},
                                                                ("qB","b",0):{tuple()},
                                                                ("qT","",1):{("qR",)},
                                                                ("qR","",1):{("qS",)}})
        closure = {
            ("qA"): {"qA"},
            ("qB"): {"qB"},
            ("qS"): {"qS"},
            ("qT"): {"qT","qR","qS"},
            ("qR"): {"qR","qS"}
        }
        self.assertEqual(automaton.get_epsilon_closure(), closure)

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(NTTATests)
    runner = unittest.TextTestRunner()
    result = runner.run(suite)
    print(result)