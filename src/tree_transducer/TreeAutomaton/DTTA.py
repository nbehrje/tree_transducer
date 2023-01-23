"""
Deterministic Top-down Tree Automaton Module
"""
from collections.abc import Iterable
from ..Tree import Tree
from .TreeAutomaton import TreeAutomaton

class DFTTA(TreeAutomaton):
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