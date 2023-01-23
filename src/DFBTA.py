"""
Deterministic Bottom-up Tree Automaton Module
"""
from collections.abc import Iterable
import src.Tree as Tree

class DFBTA:
    """
    Deterministic bottom-up finite-state tree automaton
    """

    def __init__(self, states: Iterable, final_states: Iterable, symbols: Iterable, transitions: dict):
        """Creates a deterministic finite state tree automaton
        
        Args:
            states: An Iterable containing the set of states (Q)
            final_states: An Iterable containing the set of final states (Q_f)
            symbols: An Iterable containing the set of symbols (F)
            transitions: A dict containing the transitions (Delta)

        Raises:
            ValueError: The DFBTA is not properly defined.
        """
        self.states = set(states)
        self.final_states = set(final_states)
        self.symbols = set(symbols)
        self.transitions = transitions
            
        self._validate_input()

    def _validate_input(self):
        """Verifies that the arguments passed to init produce a well-defined automaton
        
        Raises:
            ValueError: The DFBTA is not properly defined.
        """
        #Verify states
        if not self.final_states.issubset(self.states):
            raise ValueError("final_states must be a subset of states.")

        #Verify transitions
        transitions_states = set(sum({k[0] for k in self.transitions.keys()}, ())).union(set(self.transitions.values()))
        transitions_symbols = {k[1] for k in self.transitions.keys()}
        if not transitions_states.issubset(self.states):
            raise ValueError(f"DFBTA's transitions contain state(s) not present in DFBTA's states: {transitions_states - self.states}")
        if not transitions_symbols.issubset(self.symbols):
            raise ValueError(f"DFBTA's transitions contain symbol(s) not present in DFBTA's symbols: {transitions_symbols - self.symbols}")

    def accepts(self, tree: Tree) -> bool:
        """Checks whether a tree is accepted by the DFBTA

        Args:
            tree: The candidate Tree.

        Returns:
            bool: True if the DFBTA accepts the tree and False otherwise.
        """
        final_state = self._accept_helper(tree)
        return final_state in self.final_states

    def _accept_helper(self, tree: Tree):
        """Recursive helper for accept()

        Args:
            tree: The candidate Tree.

        Returns:
            The state of the input Tree when processed by the utomaton
        """
        child_states = tuple(self._accept_helper(c) for c in tree.children)
        return self.transitions.get((child_states, tree.value), None)

