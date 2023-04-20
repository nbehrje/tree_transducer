import unittest
from src.tree_transducer.TreeAutomaton.DBTA import DBTA
from src.tree_transducer.Tree import Tree

class DBTATests(unittest.TestCase):
    #Raises error if DBTA's final states is not a subset of the DBTA's states
    def testFinalStatesNotSubset(self):
        self.assertRaises(ValueError, DBTA, [], ["qA"], [], [])

    #Raises error if DBTA's transitions contain states or symbols not present in the DBTA's states or symbols
    def testNewStatesSymbolsInTransitions(self):
        self.assertRaises(ValueError, DBTA, ["qA"], ["qA"], ["A"], {(("qA",), "A"): {"qA"},(("qB",), "A"): {"qA"}})
        self.assertRaises(ValueError, DBTA, ["qA"], ["qA"], ["A"], {(("qA",), "A"): {"qA"},(("qA",), "B"): {"qA"}})

    #Returns True if the tree is accepted
    def testCorrectTreeAccepted(self):
        automaton = DBTA(["qA"],["qA"],["A"],{(("qA","qA"),"A"):{"qA"}, (tuple(),"A"):{"qA"}})
        tree = Tree("A", [Tree("A"), Tree("A", [Tree("A"), Tree("A")])])
        self.assertTrue(automaton.accepts(tree))

    #Returns False if the tree is rejected
    def testIncorrectTreeRejected(self):
        automaton = DBTA(["qA"],["qA"],["A"],{(("qA","qA"),"A"):{"qA"}, (tuple(),"A"):{"qA"}})
        tree = Tree("A", [Tree("A"), Tree("A", [Tree("A")])])
        self.assertFalse(automaton.accepts(tree))

    #Raises error if there is an epsilon transition
    def testEpsilon(self):
        self.assertRaises(ValueError, DBTA, ["qA"], ["qA"], ["A"], {(("qA",), ""): {"qA"}})

    #Raises error if there are multiple transitions for a set of states and a symbol
    def testNondeterministic(self):
        self.assertRaises(ValueError, DBTA, ["qA", "qB"], ["qA"], ["A"], {(("qA",), ""): {"qA", "qB"}})

    #Returns minimized automaton
    def testMinimize(self):
        automaton = DBTA(["qA","qB","qC"],["qA"], ["A","B","C"], {(("qA",),"A"): {"qA"},
                                                         (tuple(),"A"): {"qA"},
                                                         (tuple(),"B"): {"qB"},
                                                         (("qB",),"B"): {"qB"},
                                                         (tuple(),"C"): {"qC"},
                                                         (("qC","qC"),"C"): {"qC"}
                                                        })
        minimized = DBTA(["qA","qB_qC"],["qA"], ["A","B","C"], {(('qA',), 'A'): {'qA'},
                                                                  ((), 'A'): {'qA'},
                                                                  ((), 'B'): {'qB_qC'},
                                                                  (('qB_qC',), 'B'): {'qB_qC'},
                                                                  ((), 'C'): {'qB_qC'},
                                                                  (('qB_qC', 'qB_qC'), 'C'): {'qB_qC'}})
        self.assertEqual(automaton.minimize(), minimized)

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(DBTATests)
    runner = unittest.TextTestRunner()
    result = runner.run(suite)
    print(result)