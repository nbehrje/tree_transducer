"""
Tree Automaton class
"""
from collections.abc import Iterable
from ..Tree import Tree

class TreeAutomaton:
    """
    Tree automaton module. The types of tree automata inherit from this.
    """

    def __init__(self, states: Iterable, final_states: Iterable, symbols: Iterable, transitions: dict):
        """Creates an automaton
        
        Args:
            states: An Iterable containing the set of states (Q)
            final_states: An Iterable containing the set of final states (Q_{f/i})
            symbols: An Iterable containing the set of symbols (F)
            transitions: A dict containing the transitions (Delta)
        """
        self.states = set(states)
        self.final_states = set(final_states)
        self.symbols = set(symbols)
        self.transitions = transitions
            
        self._validate_input()

    def accepts(self, tree: Tree) -> bool:
        """Checks whether a tree is accepted by the automaton

        Args:
            tree: The candidate Tree.

        Returns:
            bool: True if the DFBTA accepts the tree and False otherwise.
        """
        final_state = self._accept_helper(tree)
        return final_state in self.final_states