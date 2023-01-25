"""
Tree Transducer module
"""
from collections.abc import Iterable
from ..Tree import Tree

class TreeTransducer:
    """
    Tree transducer class. The types of tree transducers inherit from this.
    """
    def __init__(self, states: Iterable, final_states: Iterable, in_symbols: Iterable, out_symbols: Iterable, transitions: dict):
        """
        Creates a tree transducer

        Args:
            states: An Iterable containing the set of states (Q)
            final_states: An Iterable containing the set of final states (Q_{f/i})
            in_symbols: An Iterable containing the set of input symbols (F)
            out_symbols: An Iterable containing the set of output symbols (F')
            transitions: A dict containing the transitions (Delta)
        """
        self.states = set(states)
        self.final_states = set(final_states)
        self.in_symbols = set(in_symbols)
        self.out_symbols = set(out_symbols)
        self.transitions = transitions
            
        self._validate_input()

    def _validate_input(self):
        """
        Verifies that the arguments passed to init produce a well-defined transducer.
        This method is intended to be overridden by subclasses of TreeTransducer.
        """
        raise NotImplementedError

    def transduce(self, tree: Tree) -> Tree:
        """
        Transduces the input Tree.

        Args:
            tree: The Tree to be transduced.

        This method is intended to be overridden by subclasses of TreeAutomaton.
        """
        raise NotImplementedError