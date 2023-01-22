"""
Deterministic Bottom-up Tree Automaton Module
"""
from collections.abc import Iterable

class DFBTA:
    """
    Deterministic bottom-up finite-state tree automaton
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

        Raises:
            ValueError: The DFBTA is not properly defined.
        """
        self.states = set(states)
        self.final_states = set(final_states)
        self.symbols = set(symbols)
        self.rules = set(rules)

        self.validate_input()

    def validate_input(self):
        #Verify states
        if not self.final_states.issubset(self.states):
            raise ValueError("final_states must be a subset of states.")

        #Verify rules
        rules_unzipped = list(zip(*self.rules))
        rules_states = set(rules_unzipped[0])
        rules_symbols = set(rules_unzipped[1])
        if not rules_states.issubset(self.states):
            raise ValueError(f"DFBTA's rules contain state(s) not present in DFBTA's states: {rules_states - self.states}")
        if not rules_symbols.issubset(self.symbols):
            raise ValueError(f"DFBTA's rules contain symbol(s) not present in DFBTA's symbols: {rules_symbols - self.symbols}")