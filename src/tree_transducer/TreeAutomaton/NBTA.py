"""
Non-deterministic Bottom-up Tree Automaton Module
"""
from collections.abc import Iterable
from ..Tree import Tree
from .TreeAutomaton import TreeAutomaton
from itertools import product

class NBTA(TreeAutomaton):
    """
    Non-deterministic bottom-up finite-state tree automaton
    """

    def __init__(self, states: Iterable, final_states: Iterable, symbols: Iterable, transitions: dict):
        """
        Creates a non-deterministic finite-state bottom-up tree automaton
        
        Args:
            states: An Iterable containing the set of states (Q)
            final_states: An Iterable containing the set of final states (Q_f)
            symbols: An Iterable containing the set of symbols (F)
            transitions: A dict containing the transitions (Delta)

        Raises:
            ValueError: The DBTA is not properly defined.
        """
        super().__init__(states, final_states, symbols, transitions)

    def _validate_input(self):
        """
        Verifies that the arguments passed to init produce a well-defined automaton
        
        Raises:
            ValueError: The NBTA is not properly defined.
        """
        #Verify states
        if not self.final_states.issubset(self.states):
            raise ValueError("final_states must be a subset of states.")

        #Verify transitions
        transitions_states = set()
        transitions_symbols = set()
        for (k, v) in self.transitions.items():
            transitions_states.update(set(k[0]))
            transitions_states.update(v)
            if k[1]:
                transitions_symbols.add(k[1])
        if not transitions_states.issubset(self.states):
            raise ValueError(f"NBTA's transitions contain state(s) not present in its states: {transitions_states - self.states}")
        if not transitions_symbols.issubset(self.symbols):
            raise ValueError(f"NBTA's transitions contain symbol(s) not present in its symbols: {transitions_symbols - self.symbols}")

    def accepts(self, tree: Tree) -> bool:
        """
        Checks whether a tree is accepted by the automaton

        Args:
            tree: The candidate Tree.

        Returns:
            bool: True if the DBTA accepts the tree and False otherwise.
        """
        final_state = self._accept_helper(tree)
        return final_state.intersection(self.final_states) != set()

    def _accept_helper(self, tree: Tree):
        """
        Recursive helper for accept()

        Args:
            tree: The candidate Tree.

        Returns:
            The state of the input Tree when processed by the automaton
        """
        child_states = tuple(self._accept_helper(c) for c in tree.children)
        child_possibilities = set(product(*child_states))
        states_epsilon = [self.transitions.get((children, ""), set()) for children in child_possibilities]
        states_read = [self.transitions.get((children, tree.value), set()) for children in child_possibilities]
        states = states_epsilon + states_read
        if states:
            return set.union(*states)
        return set()