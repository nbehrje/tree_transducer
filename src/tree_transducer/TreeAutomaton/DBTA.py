"""
Deterministic Bottom-up Tree Automaton Module
"""
from collections.abc import Iterable
from ..Tree import Tree
from .NBTA import NBTA

class DBTA(NBTA):
    def _validate_input(self):
        """
        Verifies that the arguments passed to init produce a well-defined automaton
        
        Raises:
            ValueError: The automaton is not properly defined.
        """
        super()._validate_input()
        for (k, v) in self.transitions.items():
            if len(v) > 1:
                raise ValueError("Deterministic automaton contains transition to multiple states")
            if not k[1]:
                raise ValueError("Deterministic automaton contains epsilon transition")