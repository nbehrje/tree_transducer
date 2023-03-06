import unittest
from src.tree_transducer.TreeTransducer.NBTT import NBTT
from src.tree_transducer.Tree import Tree, VarLeaf

class NBTTTests(unittest.TestCase):
    #Raises error if NBTT's final states is not a subset of the NBTT's states
    def testFinalStatesNotSubset(self):
        self.assertRaises(ValueError, NBTT, [], ["qA"], [], [], {})

    #Raises error if NBTT's transitions contain states or symbols not present in the NBTT's states or symbols
    def testNewStatesSymbolsInTransitions(self):
        self.assertRaises(ValueError, NBTT, ["qA"],["qA"],["A"],["Z"],{(("qB",),"A"):[("qA",Tree("Z"))]})
        self.assertRaises(ValueError, NBTT, ["qA"],["qA"],["A"],["Z"],{(("qA",),"B"):[("qA",Tree("Z"))]})
        self.assertRaises(ValueError, NBTT, ["qA"],["qA"],["A"],["Z"],{(("qA",),"A"):[("qB",Tree("Z"))]})
        self.assertRaises(ValueError, NBTT, ["qA"],["qA"],["A"],["Z"],{(("qB",),"A"):[("qA",Tree("Y"))]})

    #Returns correctly-transduced tree
    def testCorrectTransduction(self):
        transducer = NBTT(["qS","qA","qB"],["qS"],["A","B","S"],["A","B","S"],{
                                                        (("qA","qB"),"S"):[("qS",Tree("S", [VarLeaf(1), VarLeaf(0)]))],
                                                        (("qA","qS","qB"),"S"):[("qS", Tree("S", [VarLeaf(2), VarLeaf(1), VarLeaf(0)]))],
                                                        (tuple(), "A"):[("qA", Tree("A"))],
                                                        (tuple(), "B"):[("qB", Tree("B"))]})
        in_tree = Tree("S", [Tree("A"), Tree("S", [Tree("A"), Tree("B")]), Tree("B")])
        out_trees = [Tree("S", [Tree("B"), Tree("S", [Tree("B"), Tree("A")]), Tree("A")])]
        self.assertEqual(transducer.transduce(in_tree), out_trees)
        transducer = NBTT(["qS","qA","qB"],["qS"],["A","B","S"],["A","B","S"],{
                                                        (("qA","qB"),"S"):[("qS",Tree("S", [VarLeaf(1), VarLeaf(0)])),("qS",Tree("S", [VarLeaf(0), VarLeaf(1)]))],
                                                        (("qA","qS","qB"),"S"):[("qS", Tree("S", [VarLeaf(2), VarLeaf(1), VarLeaf(0)])),("qS", Tree("S", [VarLeaf(0), VarLeaf(1), VarLeaf(2)]))],
                                                        (tuple(), "A"):[("qA", Tree("A"))],
                                                        (tuple(), "B"):[("qB", Tree("B"))]})
        in_tree = Tree("S", [Tree("A"), Tree("S", [Tree("A"), Tree("B")]), Tree("B")])
        out_trees = set([in_tree,
                    Tree("S", [Tree("B"), Tree("S", [Tree("B"), Tree("A")]), Tree("A")]),
                    Tree("S", [Tree("B"), Tree("S", [Tree("A"), Tree("B")]), Tree("A")]),
                    Tree("S", [Tree("A"), Tree("S", [Tree("B"), Tree("A")]), Tree("B")])])
        self.assertEqual(set(transducer.transduce(in_tree)), out_trees)
        transducer = NBTT(["qS","qA","qB","qR","qT"],["qT"],["A","B","S"],["A","B","S","R","T"],{
                                                        (("qA","qB"),"S"):[("qS",Tree("S", [VarLeaf(1), VarLeaf(0)]))],
                                                        (tuple(), "A"):[("qA", Tree("A"))],
                                                        (tuple(), "B"):[("qB", Tree("B"))],
                                                        (("qS",),""):[("qR", Tree("R", [VarLeaf(0)]))],
                                                        (("qR",),""):[("qT", Tree("T", [VarLeaf(0)]))],
                                                        (("qA","qR","qB"),"S"):[("qS", Tree("S", [VarLeaf(2), VarLeaf(1), VarLeaf(0)]))]})
        in_tree = Tree("S", [Tree("A"), Tree("S", [Tree("A"), Tree("B")]), Tree("B")])
        out_trees = [Tree("T", [Tree("R", [Tree("S", [Tree("B"), Tree("R", [Tree("S", [Tree("B"), Tree("A")])]), Tree("A")])])])]
        self.assertEqual(transducer.transduce(in_tree), out_trees)

    #Returns epsilon closure
    def testEpsilonClosure(self):
        transducer = NBTT(["qS","qA","qB","qT","qR"],["qT"],["A","B","S"],["A","B","S"],{
                                                        (("qA","qB"),"S"):[("qS",Tree("S", [VarLeaf(1), VarLeaf(0)]))],
                                                        (("qA","qS","qB"),"S"):[("qS", Tree("S", [VarLeaf(2), VarLeaf(1), VarLeaf(0)]))],
                                                        (("qS",), ""):[("qR", VarLeaf(0))],
                                                        (("qR",), ""):[("qT", VarLeaf(0))]})
        closure = {
            "qA": {"qA"},
            "qB": {"qB"},
            "qS": {"qS", "qR", "qT"},
            "qR": {"qR", "qT"},
            "qT": {"qT"}
        }
        self.assertEqual(transducer.get_epsilon_closure(), closure)

    #Returns union
    def testUnion(self):
        transducer1 = NBTT(["qS","qA","qB"],["qS"],["a","b","S"],["a","b","S"], {(("qA","qB"),"S"):[("qS",Tree("S", [VarLeaf(0),VarLeaf(1)]))], (tuple(),"a"):[("qA",Tree("a"))], (tuple(),"b"):[("qB",Tree("b"))]})
        transducer2 = NBTT(["qC"],["qC"],["C"],["C","D"], {(("qC",),"C"):[("qC",Tree("C",[VarLeaf(0)])),("qC",Tree("D",[VarLeaf(0)]))], (tuple(),"C"):[("qC",Tree("C"))]})
        union = NBTT({"qA_%S%", "qS_qC", "qA_qC", "qB_%S%", "qS_%S%", "qB_qC", "%S%_qC"},
                    {"qS_qC", "qA_qC", "qS_%S%", "qB_qC", "%S%_qC"}, 
                    ["a","b","S","C"],
                    ["a","b","S","C","D"],
                    {(("qA_%S%", "qB_%S%"), "S"): [("qS_%S%", Tree("S", [VarLeaf(0),VarLeaf(1)]))],
                        (tuple(), "a"): [("qA_%S%", Tree("a"))],
                        (tuple(), "b"): [("qB_%S%", Tree("b"))],
                        (tuple(), "C"): [("%S%_qC", Tree("C"))],
                        (("%S%_qC",), "C"): [("%S%_qC", Tree("C", [VarLeaf(0)])),("%S%_qC", Tree("D", [VarLeaf(0)]))]}
        )
        self.assertEqual(transducer1.union(transducer2), union)


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(NBTTTests)
    runner = unittest.TextTestRunner()
    result = runner.run(suite)
    print(result)