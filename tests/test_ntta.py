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

    #Returns union
    def testUnion(self):
        automaton1 = NTTA(["qA"],["qA"],["A"], {("qA","A",2):{("qA","qA")}, ("qA","A",0):{tuple()}})
        automaton2 = NTTA(["qB"],["qB"],["B"], {("qB","B",1):{("qB",)}, ("qB","B",0):{tuple()}})
        union = NTTA(["1_qA","2_qB"], ["1_qA","2_qB"], ["A","B"], {('1_qA', 'A', 2): {('1_qA', '1_qA')}, 
            ('1_qA', 'A', 0): {()},
            ('2_qB', 'B', 1):{('2_qB',)},
            ('2_qB', 'B', 0): {()}}) 
        self.assertEqual(automaton1.union(automaton2), union)

    #Returns intersection
    def testIntersection(self):
        automaton1 = NTTA(["qA","qB"],["qA"],["A","B"], {("qA","A",1):{("qA",),("qB",)}, ("qA","A",0):{tuple()}})
        automaton2 = NTTA(["qC"],["qC"],["A"], {("qC","A",1):{("qC",)}, ("qC","A",0):{tuple()}})
        intersection = NTTA(['qA_qC','qB_qC'],
                            ['qA_qC'],
                            ["A"],
                            {('qA_qC', 'A', 1): {("qA_qC",),("qB_qC",)},
                            ("qA_qC","A",0):{tuple()}}
        )
        self.assertEqual(automaton1.intersection(automaton2), intersection)

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(NTTATests)
    runner = unittest.TextTestRunner()
    result = runner.run(suite)
    print(result)