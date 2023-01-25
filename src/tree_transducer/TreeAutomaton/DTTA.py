"""
Deterministic Top-down Tree Automaton Module
"""
from collections.abc import Iterable
from ..Tree import Tree
from .TreeAutomaton import TreeAutomaton

class DTTA(TreeAutomaton):
    """
    Deterministic top-down finite-state tree automaton
    """
    def __init__(self, states: Iterable, final_states: Iterable, symbols: Iterable, transitions: dict):
        """
        Creates a deterministic finite-state top-down tree automaton
        
        Args:
            states: An Iterable containing the set of states (Q)
            final_states: An Iterable containing the set of final states (Q_i)
            symbols: An Iterable containing the set of symbols (F)
            transitions: A dict containing the transitions (Delta)

        Raises:
            ValueError: The DTTA is not properly defined.
        """
        super().__init__(states, final_states, symbols, transitions)

    def _validate_input(self):
        """
        Verifies that the arguments passed to init produce a well-defined automaton
        
        Raises:
            ValueError: The DTTA is not properly defined.
        """
        #Verify states
        if len(self.final_states) > 1:
            raise ValueError("final_states contains more than one state.")
        if not self.final_states.issubset(self.states):
            raise ValueError("final_states must be a subset of states.")

        #Verify transitions
        transitions_states = set()
        transitions_symbols = set()
        for (k, v) in self.transitions.items():
            transitions_states.update(set(v))
            transitions_states.add(k[0])
            transitions_symbols.add(k[1])
        if not transitions_states.issubset(self.states):
            raise ValueError(f"DTTA's transitions contain state(s) not present in its states: {transitions_states - self.states}")
        if not transitions_symbols.issubset(self.symbols):
            raise ValueError(f"DTTA's transitions contain symbol(s) not present in its symbols: {transitions_symbols - self.symbols}")
        for (k,v) in self.transitions.items():
            if not k[2] == len(v):
                raise ValueError(f"DTTA's transition contains mismatched number of children: {k,v}")

    def accepts(self, tree: Tree) -> bool:
        """
        Checks whether a tree is accepted by the automaton

        Args:
            tree: The candidate Tree.

        Returns:
            bool: True if the DTTA accepts the tree and False otherwise.
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
            bool: True if the transitions on the input subtree are defined
        """
        key = (state, tree.value, len(tree.children))
        val = self.transitions.get(key, None)
        return val is not None and all(self._accept_helper(val[c],tree.children[c]) for c in range(len(tree.children)))