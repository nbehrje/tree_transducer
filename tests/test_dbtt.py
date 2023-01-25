import unittest
from src.tree_transducer.TreeTransducer.DBTT import DBTT
from src.tree_transducer.Tree import Tree, VarLeaf

class DBTTTests(unittest.TestCase):
    #Raises error if DBTA's final states is not a subset of the DTTA's states
    def testFinalStatesNotSubset(self):
        self.assertRaises(ValueError, DBTT, [], ["qA"], [], [], {})

    #Raises error if DBTT's transitions contain states or symbols not present in the DBTT's states or symbols
    def testNewStatesSymbolsInTransitions(self):
        self.assertRaises(ValueError, DBTT, ["qA"],["qA"],["A"],["Z"],{(("qB",),"A"):("qA",Tree("Z", VarLeaf(0)))})
        self.assertRaises(ValueError, DBTT, ["qA"],["qA"],["A"],["Z"],{(("qA",),"B"):("qA",Tree("Z", VarLeaf(0)))})
        self.assertRaises(ValueError, DBTT, ["qA"],["qA"],["A"],["Z"],{(("qA",),"A"):("qB",Tree("Z", VarLeaf(0)))})
        self.assertRaises(ValueError, DBTT, ["qA"],["qA"],["A"],["Z"],{(("qB",),"A"):("qA",Tree("Y", VarLeaf(0)))})

    #Returns correctly-transduced tree
    def testCorrectTransduction(self):
        transducer = DBTT(["qS","qA","qB"],["qS"],["A","B","S"],["A","B","S"],{
                                                        (("qA","qB"),"S"):("qS",Tree("S", [VarLeaf(1), VarLeaf(0)])),
                                                        (("qA","qS","qB"),"S"):("qS", Tree("S", [VarLeaf(2), VarLeaf(1), VarLeaf(0)])),
                                                        (tuple(), "A"):("qA", Tree("A")),
                                                        (tuple(), "B"):("qB", Tree("B"))})
        in_tree = Tree("S", [Tree("A"), Tree("S", [Tree("A"), Tree("B")]), Tree("B")])
        out_tree = Tree("S", [Tree("B"), Tree("S", [Tree("B"), Tree("A")]), Tree("A")])
        self.assertEqual(transducer.transduce(in_tree), out_tree)

    #Returns nothing if tree is not in a valid final state
    def testTransductionWrongState(self):
        transducer = DBTT(["qS","qA","qB","qT"],["qS"],["A","B","S"],["A","B","S"],{
                                                        (("qA","qB"),"S"):("qS",Tree("S", [VarLeaf(1), VarLeaf(0)])),
                                                        (("qA","qS","qB"),"S"):("qT", Tree("S", [VarLeaf(2), VarLeaf(1), VarLeaf(0)])),
                                                        (tuple(), "A"):("qA", Tree("A")),
                                                        (tuple(), "B"):("qB", Tree("B"))})
        in_tree = Tree("S", [Tree("A"), Tree("S", [Tree("A"), Tree("B")]), Tree("B")])
        self.assertEqual(transducer.transduce(in_tree), None)

    #Returns nothing if there is no valid transition for a subtree
    def testNoTransition(self):
        transducer = DBTT(["qS","qA","qB"],["qS"],["A","B","S","C"],["A","B","S"],{
                                                        (("qA","qB"),"S"):("qS",Tree("S", [VarLeaf(1), VarLeaf(0)])),
                                                        (("qA","qS","qB"),"S"):("qS", Tree("S", [VarLeaf(2), VarLeaf(1), VarLeaf(0)])),
                                                        (tuple(), "A"):("qA", Tree("A")),
                                                        (tuple(), "B"):("qB", Tree("B"))})
        in_tree = Tree("S", [Tree("A"), Tree("S", [Tree("C"), Tree("B")]), Tree("B")])
        self.assertEqual(transducer.transduce(in_tree), None)

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(DBTTTests)
    runner = unittest.TextTestRunner()
    result = runner.run(suite)
    print(result)