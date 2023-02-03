import unittest
from src.tree_transducer.TreeTransducer.DTTT import DTTT
from src.tree_transducer.Tree import Tree, VarLeaf

class DTTTTests(unittest.TestCase):
    #Raises error if DTTT's final states is not a subset of the DTTT's states
    def testFinalStatesNotSubset(self):
        self.assertRaises(ValueError, DTTT, [], ["qA"], [], [], {})

    #Raises error if DTTT's transitions contain states or symbols not present in the DTTT's states or symbols
    def testNewStatesSymbolsInTransitions(self):
        self.assertRaises(ValueError, DTTT, ["qA"],["qA"],["A"],["Z"],{("qB","A", 1):(("qA",),Tree("Z", [VarLeaf(0)]))})
        self.assertRaises(ValueError, DTTT, ["qA"],["qA"],["A"],["Z"],{("qA","B", 1):(("qA",),Tree("Z", [VarLeaf(0)]))})
        self.assertRaises(ValueError, DTTT, ["qA"],["qA"],["A"],["Z"],{("qA","A", 1):(("qB",),Tree("Z", [VarLeaf(0)]))})
        self.assertRaises(ValueError, DTTT, ["qA"],["qA"],["A"],["Z"],{("qA","A", 1):(("qA","qA"),Tree("Z", [Tree("Y"), VarLeaf(0)]))})

    #Returns correctly-transduced tree
    def testCorrectTransduction(self):
        transducer = DTTT(["qS","qA","qB"],["qS"],["A","B","S"],["A","B","S"],{
                        ("qS", "S", 2):(("qA","qB"),Tree("S", [VarLeaf(1), VarLeaf(0)])),
                        ("qS", "S", 3):(("qA","qS","qB"),Tree("S", [VarLeaf(2), VarLeaf(1), VarLeaf(0)])),
                        ("qB", "B", 0):(tuple(),Tree("B")),
                        ("qA", "A", 0):(tuple(),Tree("A"))
                        })
        in_tree = Tree("S", [Tree("A"), Tree("S", [Tree("A"), Tree("B")]), Tree("B")])
        out_tree = Tree("S", [Tree("B"), Tree("S", [Tree("B"), Tree("A")]), Tree("A")])
        self.assertEqual(transducer.transduce(in_tree), out_tree)

    #Returns nothing if there is no valid transition for a subtree
    def testNoTransduction(self):
        transducer = DTTT(["qS","qA","qB"],["qS"],["A","B","S"],["A","B","S"],{
                        ("qS", "S", 2):(("qA","qB"),Tree("S", [VarLeaf(1), VarLeaf(0)])),
                        ("qS", "S", 3):(("qA","qS","qB"),Tree("S", [VarLeaf(2), VarLeaf(1), VarLeaf(0)])),
                        ("qB", "B", 0):(tuple(),Tree("B")),
                        ("qA", "A", 0):(tuple(),Tree("A"))
                        })
        in_tree = Tree("S", [Tree("A"), Tree("S", [Tree("A")]), Tree("B")])
        self.assertEqual(transducer.transduce(in_tree), None)

    #Raises error if there is an epsilon transition
    def testEpsilon(self):
        self.assertRaises(ValueError, DTTT, ["qA"],["qA"],["A"],["Z"],{("qB","", 1):(("qA",),Tree("Z", [VarLeaf(0)]))})

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(DTTTTests)
    runner = unittest.TextTestRunner()
    result = runner.run(suite)
    print(result)