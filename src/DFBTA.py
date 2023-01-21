"""
dfbta module
"""
from collections.abc import Iterable

class DFBTA:
    """
    Deterministic bottom-up finite-state automaton
    """

    def __init__(self, states: Iterable, final_states: Iterable, symbols: Iterable, rules: Iterable[tuple]):
        """Creates a deterministic finite state tree automaton
        
        Args:
            states:
                An iterable containing the set of states (Q)
            final_states:
                An iterable containing the set of final states (Q_f)
            symbols:
                An iterable containing the set of symbols (F)
            rules:
                An iterable of tuples containing the set of rules (Delta)

        Returns:
            A deterministic finite state tree automaton
        """
        self.states = set(states)
        self.final_states = set(final_states)
        self.symbols = set(symbols)
        self.rules = set(rules)

        self.validate_input(states, final_states, symbols, rules)

    def validate_input(self, states: set, final_states: set, symbols: set, rules: set[tuple]):
        self.validate_states(states, final_states)

    def validate_states(self, states: set, final_states: set):
        if not states:
            raise ValueError("states must not be empty")