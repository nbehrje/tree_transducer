"""
Deterministic finite-state top-down tree transducer module
"""
from collections.abc import Iterable
from .NTTT import NTTT
from src.tree_transducer.Tree import Tree, VarLeaf

class DTTT(NTTT):
    """
    Deterministic finite-state bottom-up tree transducer class
    """

    def _validate_input(self):
        """
        Verifies that the arguments passed to init produce a well-defined transducer
        
        Raises:
            ValueError: The DTTT is not properly defined.
        """
        super()._validate_input()
        for (k, v) in self.transitions.items():
            if len(v) > 1:
                raise ValueError("Deterministic transducer contains multiple transitions for one symbol")
            if not k[1]:
                raise ValueError("Deterministic transducer contains epsilon transition")