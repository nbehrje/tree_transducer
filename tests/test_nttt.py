import unittest
from src.tree_transducer.TreeTransducer.NTTT import NTTT
from src.tree_transducer.Tree import Tree, VarLeaf

class NTTTTests(unittest.TestCase):
    #Raises error if NTTT's final states is not a subset of the DTTT's states
    def testFinalStatesNotSubset(self):
        self.assertRaises(ValueError, NTTT, [], ["qA"], [], [], {})

    #Raises error if NTTT's transitions contain states or symbols not present in the NTTT's states or symbols
    def testNewStatesSymbolsInTransitions(self):
        self.assertRaises(ValueError, NTTT, ["qA"],["qA"],["A"],["Z"],{("qB","A", 1):{(("qA",),Tree("Z", [VarLeaf(0)]))}})
        self.assertRaises(ValueError, NTTT, ["qA"],["qA"],["A"],["Z"],{("qA","B", 1):{(("qA",),Tree("Z", [VarLeaf(0)]))}})
        self.assertRaises(ValueError, NTTT, ["qA"],["qA"],["A"],["Z"],{("qA","A", 1):{(("qB",),Tree("Z", [VarLeaf(0)]))}})
        self.assertRaises(ValueError, NTTT, ["qA"],["qA"],["A"],["Z"],{("qA","A", 1):{(("qA","qA"),Tree("Z", [Tree("Y"), VarLeaf(0)]))}})

    #Returns correctly-transduced tree
    def testCorrectTransduction(self):
        transducer = NTTT(["qS","qA","qB"],["qS"],["A","B","S"],["A","B","S"],{
                        ("qS", "S", 2):{(("qA","qB"),Tree("S", [VarLeaf(1), VarLeaf(0)]))},
                        ("qS", "S", 3):{(("qA","qS","qB"),Tree("S", [VarLeaf(2), VarLeaf(1), VarLeaf(0)]))},
                        ("qB", "B", 0):{(tuple(),Tree("B"))},
                        ("qA", "A", 0):{(tuple(),Tree("A"))}
                        })
        in_tree = Tree("S", [Tree("A"), Tree("S", [Tree("A"), Tree("B")]), Tree("B")])
        out_tree = {Tree("S", [Tree("B"), Tree("S", [Tree("B"), Tree("A")]), Tree("A")])}
        #self.assertEqual(transducer.transduce(in_tree), out_tree)
        transducer = NTTT(["qS","qA","qB"],["qS"],["A","B","S"],["A","B","S"],{
                        ("qS", "S", 2):{(("qA","qB"),Tree("S", [VarLeaf(1), VarLeaf(0)])),(("qA","qB"),Tree("S", [VarLeaf(0), VarLeaf(1)]))},
                        ("qS", "S", 3):{(("qA","qS","qB"),Tree("S", [VarLeaf(2), VarLeaf(1), VarLeaf(0)])),(("qA","qS","qB"),Tree("S", [VarLeaf(0), VarLeaf(1), VarLeaf(2)]))},
                        ("qB", "B", 0):{(tuple(),Tree("B"))},
                        ("qA", "A", 0):{(tuple(),Tree("A"))}
                        })
        in_tree = Tree("S", [Tree("A"), Tree("S", [Tree("A"), Tree("B")]), Tree("B")])
        out_tree = {Tree("S", [Tree("B"), Tree("S", [Tree("B"), Tree("A")]), Tree("A")]),
                    Tree("S", [Tree("B"), Tree("S", [Tree("A"), Tree("B")]), Tree("A")]),
                    Tree("S", [Tree("A"), Tree("S", [Tree("B"), Tree("A")]), Tree("B")]),
                    Tree("S", [Tree("A"), Tree("S", [Tree("A"), Tree("B")]), Tree("B")])}
        #self.assertEqual(transducer.transduce(in_tree), out_tree)
        transducer = NTTT(["qS","qA","qB","qT","qR"],["qT","qR"],["A","B","S"],["A","B","S","R","T"],{
                        ("qS", "S", 2):{(("qA","qB"),Tree("S", [VarLeaf(0), VarLeaf(1)]))},
                        ("qS", "S", 3):{(("qA","qS","qB"),Tree("S", [VarLeaf(0), VarLeaf(1), VarLeaf(2)]))},
                        ("qB", "B", 0):{(tuple(),Tree("B"))},
                        ("qA", "A", 0):{(tuple(),Tree("A"))},
                        ("qT", "", 1):{(("qR",),Tree("T", [VarLeaf(0)]))},
                        ("qR", "", 1):{(("qS",),Tree("R", [VarLeaf(0)]))}
                        })
        in_tree = Tree("S", [Tree("A"), Tree("S", [Tree("A"), Tree("B")]), Tree("B")])
        out_tree = {Tree("T", [Tree("R", [Tree("S", [Tree("A"), Tree("S", [Tree("A"), Tree("B")]), Tree("B")])])]),
                    Tree("R", [Tree("S", [Tree("A"), Tree("S", [Tree("A"), Tree("B")]), Tree("B")])])}
        self.assertEqual(transducer.transduce(in_tree), out_tree)

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(NTTTTests)
    runner = unittest.TextTestRunner()
    result = runner.run(suite)
    print(result)