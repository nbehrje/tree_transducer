"""
Deterministic Bottom-up Tree Automaton Module
"""
from collections.abc import Iterable

class DFBTA:
    """
    Deterministic bottom-up finite-state tree automaton
    """

    def __init__(self, states: Iterable, final_states: Iterable, symbols: Iterable, transitions: dict):
        """Creates a deterministic finite state tree automaton
        
        Args:
            states:
                An iterable containing the set of states (Q)
            final_states:
                An iterable containing the set of final states (Q_f)
            symbols:
                An iterable containing the set of symbols (F)
            transitions:
                A dict containing the transitions (Delta)

        Raises:
            ValueError: The DFBTA is not properly defined.
        """
        self.states = set(states)
        self.final_states = set(final_states)
        self.symbols = set(symbols)
        self.transitions = transitions
            
        self.validate_input()

    def validate_input(self):
        #Verify states
        if not self.final_states.issubset(self.states):
            raise ValueError("final_states must be a subset of states.")

        #Verify transitions
        transitions_states = {k[0] for k in self.transitions.keys()}.union(set(self.transitions.values()))
        transitions_symbols = {k[1] for k in self.transitions.keys()}
        if not transitions_states.issubset(self.states):
            raise ValueError(f"DFBTA's transitions contain state(s) not present in DFBTA's states: {transitions_states - self.states}")
        if not transitions_symbols.issubset(self.symbols):
            raise ValueError(f"DFBTA's transitions contain symbol(s) not present in DFBTA's symbols: {transitions_symbols - self.symbols}")