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

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(NBTATests)
    runner = unittest.TextTestRunner()
    result = runner.run(suite)
    print(result)