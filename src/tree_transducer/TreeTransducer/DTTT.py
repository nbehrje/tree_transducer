"""
Deterministic finite-state top-down tree transducer module
"""
from collections.abc import Iterable
from .TreeTransducer import TreeTransducer
from src.tree_transducer.Tree import Tree, VarLeaf

class DTTT(TreeTransducer):
    """
    Deterministic finite-state bottom-up tree transducer class
    """
    def __init__(self, states: Iterable, final_states: Iterable, in_symbols: Iterable, out_symbols: Iterable, transitions: dict):
        """
        Creates a tree transducer

        Args:
            states: An Iterable containing the set of states (Q)
            final_states: An Iterable containing the set of final states (Q_{f/i})
            in_symbols: An Iterable containing the set of input symbols (F)
            out_symbols: An Iterable containing the set of output symbols (F')
            transitions: A dict containing the transitions (Delta)
        """
        super().__init__(states, final_states, in_symbols, out_symbols, transitions)

    def _validate_input(self):
        """
        Verifies that the arguments passed to init produce a well-defined transducer
        
        Raises:
            ValueError: The DTTT is not properly defined.
        """
        #Verify states
        if not self.final_states.issubset(self.states):
            raise ValueError("final_states must be a subset of states.")

        #Verify transitions
        transitions_states = set()
        transitions_in_symbols = set()
        transitions_out_symbols = set()
        for (k, v) in self.transitions.items():
            transitions_states.add(k[0])
            transitions_states.update(v[0])
            transitions_in_symbols.add(k[1])
            transitions_out_symbols.update(v[1].get_values())
        if not transitions_states.issubset(self.states):
            raise ValueError(f"DTTT's transitions contain state(s) not present in its states: {transitions_states - self.states}")
        if not transitions_in_symbols.issubset(self.in_symbols):
            raise ValueError(f"DTTT's transitions contain input symbol(s) not present in its in_symbols: {transitions_in_symbols - self.in_symbols}")
        if not transitions_out_symbols.issubset(self.out_symbols):
            raise ValueError(f"DTTT's transitions contain output symbol(s) not present in its out_symbols: {transitions_out_symbols - self.out_symbols}")

    def transduce(self, tree: Tree) -> Tree:
        """
        Transduces the input Tree.

        Args: 
            tree: The Tree to be transduced.

        Returns:
            Tree: A new Tree made by applying the transduction to the input Tree
        """
        root_state = next(iter(self.final_states))
        return self._transduce_helper(root_state, tree)

    def _transduce_helper(self, state, in_tree: Tree) -> Tree:
        """
        Recursive helper for transduce()

        Args:
            state: The state of the tree.
            tree: The Tree to be transduced.

        Returns:
            Tree: The filled output Tree
        """
        num_in_children = len(in_tree.children)
        child_states, out_tree = self.transitions.get((state, in_tree.value, num_in_children), (None, None))
        if out_tree is None:
            return None
        child_trees = [self._transduce_helper(child_states[i], in_tree.children[i]) for i in range(num_in_children)]
        if None in child_trees:
            return None
        out_tree = out_tree.fill(child_trees)
        return out_tree