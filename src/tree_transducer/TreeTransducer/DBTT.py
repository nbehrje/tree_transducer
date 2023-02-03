"""
Deterministic finite-state bottom-up tree transducer module
"""
from collections.abc import Iterable
from .TreeTransducer import TreeTransducer
from src.tree_transducer.Tree import Tree

class DBTT(TreeTransducer):
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
            ValueError: The DBTT is not properly defined.
        """
        #Verify states
        if not self.final_states.issubset(self.states):
            raise ValueError("final_states must be a subset of states.")

        #Verify transitions
        transitions_states = set()
        transitions_in_symbols = set()
        transitions_out_symbols = set()
        for (k, v) in self.transitions.items():
            transitions_states.update(set(k[0]))
            transitions_states.add(v[0])
            transitions_in_symbols.add(k[1])
            transitions_out_symbols.add(v[1].value)
        if "" in self.in_symbols or "" in transitions_in_symbols:
            raise ValueError("Deterministic automaton contains an epsilon transition")
        if not transitions_states.issubset(self.states):
            raise ValueError(f"DBTT's transitions contain state(s) not present in its states: {transitions_states - self.states}")
        if not transitions_in_symbols.issubset(self.in_symbols):
            raise ValueError(f"DBTT's transitions contain input symbol(s) not present in its in_symbols: {transitions_in_symbols - self.in_symbols}")
        if not transitions_out_symbols.issubset(self.out_symbols):
            raise ValueError(f"DBTT's transitions contain output symbol(s) not present in its out_symbols: {transitions_out_symbols - self.out_symbols}")

    def transduce(self, tree: Tree) -> Tree:
        """
        Transduces the input Tree.

        Args: 
            tree: The Tree to be transduced.

        Returns:
            Tree: A new Tree made by applying the transduction to the input Tree
        """
        (out_state, out_tree) = self._transduce_helper(tree)
        if out_state in self.final_states:
            return out_tree
        return None

    def _transduce_helper(self, tree: Tree):
        """
        Recursive helper for transduce()

        Args:
            tree: The Tree to be transduced.

        Returns:
            A tuple containing a state and an output tree that has that state
        """
        if tree.is_leaf():
            child_states, child_trees = tuple(), tuple()
        else:
            children = list(zip(*[self._transduce_helper(c) for c in tree.children]))
            child_states, child_trees = children[0], children[1]
        parent_state, out_tree = self.transitions.get((child_states, tree.value), (None,None))
        if parent_state is not None:
            out_tree = out_tree.fill(child_trees)
        return (parent_state, out_tree)