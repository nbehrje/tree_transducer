import unittest
from src.tree_transducer.TreeAutomaton.NBTA import NBTA
from src.tree_transducer.Tree import Tree

class NBTATests(unittest.TestCase):
    #Raises error if NBTA's final states is not a subset of the NBTA's states
    def testFinalStatesNotSubset(self):
        self.assertRaises(ValueError, NBTA, [], ["qA"], [], [])

    #Raises error if NBTA's transitions contain states or symbols not present in the NBTA's states or symbols
    def testNewStatesSymbolsInTransitions(self):
        self.assertRaises(ValueError, NBTA, ["qA"], ["qA"], ["A"], {(("qA",), "A"): {"qA"},(("qB",), "A"): {"qA"}})
        self.assertRaises(ValueError, NBTA, ["qA"], ["qA"], ["A"], {(("qA",), "A"): {"qA"},(("qA",), "B"): {"qA"}})
        self.assertRaises(ValueError, NBTA, ["qA"], ["qA"], ["A"], {(("qA",), "A"): {"qA", "qB"}})

    #Returns True if the tree is accepted
    def testCorrectTreeAccepted(self):
        automaton = NBTA(["qA"],["qA"],["A"],{(("qA","qA"),"A"):{"qA"}, (tuple(),"A"):{"qA"}})
        tree = Tree("A", [Tree("A"), Tree("A", [Tree("A"), Tree("A")])])
        self.assertTrue(automaton.accepts(tree))
        automaton = NBTA(["qA","qB"],["qB"],["A"],{(("qA","qA"),"A"):{"qA", "qB"}, (tuple(),"A"):{"qA"}})
        tree = Tree("A", [Tree("A"), Tree("A", [Tree("A"), Tree("A")])])
        self.assertTrue(automaton.accepts(tree))
        automaton = NBTA(["qA","qB"],["qB"],["A"],{(("qA","qA"),"A"):{"qA"}, (tuple(),"A"):{"qA"}, (("qA",),""):{"qB"}})
        tree = Tree("A", [Tree("A"), Tree("A", [Tree("A"), Tree("A")])])
        self.assertTrue(automaton.accepts(tree))

    #Returns False if the tree is rejected
    def testIncorrectTreeRejected(self):
        automaton = NBTA(["qA"],["qA"],["A"],{(("qA","qA"),"A"):{"qA"}, (tuple(),"A"):{"qA"}})
        tree = Tree("A", [Tree("A"), Tree("A", [Tree("A")])])
        self.assertFalse(automaton.accepts(tree))

    #Returns epsilon closure
    def testEpsilonClosure(self):
        automaton = NBTA(["qA","qB"],["qB"],["A"],{(("qA","qA"),"A"):{"qA"}, (tuple(),"A"):{"qA"}, (("qA",),""):{"qB"}})
        closure = {
            ("qA"): {"qA","qB"},
            ("qB"): {"qB"}
        }
        self.assertEqual(automaton.get_epsilon_closure(), closure)

    #Returns union
    def testUnion(self):
        automaton1 = NBTA(["qA"],["qA"],["A"], {(("qA","qA"),"A"):{"qA"}, (tuple(),"A"):{"qA"}})
        automaton2 = NBTA(["qB"],["qB"],["B"], {(("qB",),"B"):{"qB"}, (tuple(),"B"):{"qB"}})
        union = NBTA(["qA_qB", "qA_%S%", "%S%_qB"],
                    ["qA_qB", "qA_%S%", "%S%_qB"],
                    ["A", "B"],
                    {(("qA_%S%","qA_%S%"),"A"):{"qA_%S%"},
                        (tuple(),"A"):{"qA_%S%"},
                        (("%S%_qB",),"B"):{"%S%_qB"},
                        (tuple(),"B"):{"%S%_qB"}})
        self.assertEqual(automaton1.union(automaton2), union)

    #Returns intersection
    def testIntersection(self):
        automaton1 = NBTA(["qA"],["qA"],["A"], {(("qA","qA"),"A"):{"qA"}, (tuple(),"A"):{"qA"}})
        automaton2 = NBTA(["qA"],["qA"],["A"], {(("qA",),"A"):{"qA"}, (tuple(),"A"):{"qA"}})
        intersection = NBTA(["qA_qA"],
                    ["qA_qA"],
                    ["A"],
                    {(tuple(),"A"):{"qA_qA"}})
        self.assertEqual(automaton1.intersection(automaton2), intersection)

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(NBTATests)
    runner = unittest.TextTestRunner()
    result = runner.run(suite)
    print(result)