"""
Non-deterministic Top-down Tree Automaton Module
"""
from collections.abc import Iterable
from ..Tree import Tree
from .TreeAutomaton import TreeAutomaton
from itertools import product

class NTTA(TreeAutomaton):
    """
    Non-deterministic top-down finite-state tree automaton
    """
    def __init__(self, states: Iterable, final_states: Iterable, symbols: Iterable, transitions: dict):
        """
        Creates a non-deterministic finite-state top-down tree automaton
        
        Args:
            states: An Iterable containing the set of states (Q)
            final_states: An Iterable containing the set of initial states (Q_i)
            symbols: An Iterable containing the set of symbols (F)
            transitions: A dict containing the transitions (Delta)

        Raises:
            ValueError: The NTTA is not properly defined.
        """
        super().__init__(states, final_states, symbols, transitions)

    def _validate_input(self):
        """
        Verifies that the arguments passed to init produce a well-defined automaton
        
        Raises:
            ValueError: The NTTA is not properly defined.
        """
        #Verify states
        if not self.final_states.issubset(self.states):
            raise ValueError("final_states must be a subset of states.")

        #Verify transitions
        transitions_states = set()
        transitions_symbols = set()
        for (k, v) in self.transitions.items():
            for v_i in v:
                if not k[2] == len(v_i):
                    raise ValueError(f"NTTA's transition contains mismatched number of children: {k,v_i}")
                transitions_states.update(set(v_i))
            transitions_states.add(k[0])
            transitions_symbols.add(k[1])
        if not transitions_states.issubset(self.states):
            raise ValueError(f"NTTA's transitions contain state(s) not present in its states: {transitions_states - self.states}")
        if not transitions_symbols.issubset(self.symbols):
            raise ValueError(f"NTTA's transitions contain symbol(s) not present in its symbols: {transitions_symbols - self.symbols}")

    def accepts(self, tree: Tree) -> bool:
        """
        Checks whether a tree is accepted by the automaton

        Args:
            tree: The candidate Tree.

        Returns:
            bool: True if the NTTA accepts the tree and False otherwise.
        """
        state = next(iter(self.final_states))
        return self._accept_helper(state, tree)

    def _accept_helper(self, state, tree: Tree) -> bool:
        """
        Recursive helper for accept()

        Args:
            init_state: The current state of the tree.
            tree: The candidate Tree.

        Returns:
            bool: True if some subtree is valid and False otherwise
        """
        key = (state, tree.value, len(tree.children))
        vals = self.transitions.get(key, None).union()
        return vals and any([all(self._accept_helper(val[c],tree.children[c]) for c in range(len(tree.children)))] for val in vals)