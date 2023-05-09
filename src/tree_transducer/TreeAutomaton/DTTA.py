"""
Deterministic Top-down Tree Automaton Module
"""
from collections.abc import Iterable
from ..Tree import Tree
from .NTTA import NTTA

class DTTA(NTTA):
    """
    Deterministic top-down finite-state tree automaton
    """

    def _validate_input(self):
        """
        Verifies that the arguments passed to init produce a well-defined automaton
        
        Raises:
            ValueError: The automaton is not properly defined.
        """
        super()._validate_input()
        for (k, v) in self.transitions.items():
            if len(v) > 1:
                raise ValueError("Deterministic automaton contains multiple transitions for an input")
            if not k[1]:
                raise ValueError("Deterministic automaton contains epsilon transition")
            

    def accepts(self, tree: Tree) -> bool:
        """
        Checks whether a tree is accepted by the automaton

        Args:
            tree: The candidate Tree.

        Returns:
            bool: True if the automaton accepts the tree and False otherwise.
        """
        state = next(iter(self.final_states))
        return self._accept_helper(state, tree)

    def _accept_helper(self, state, tree: Tree) -> bool:
        """
        Recursive helper for accept()

        Args:
            init_state: The current state of the tree.
            tree: The candidate Tree.

        Returns:
            bool: True if the transitions on the input subtree are defined
        """
        key = (state, tree.value, len(tree.children))
        val = self.transitions.get(key, None)
        return val is not None and all(self._accept_helper(next(iter(val))[c],tree.children[c]) for c in range(len(tree.children)))
    
    def __eq__(self, other: object) -> bool:
        if isinstance(other, DTTA):
            return self.states == other.states and \
                    self.final_states == other.final_states and \
                    self.transitions == other.transitions
        return False

    def __str__(self) -> str:
        return f"DTTA(States: {self.states}\n \
                Final States: {self.final_states}\n \
                Transitions: {self.transitions})"

    def __repr__(self) -> str:
        return f"DTTA(States: {self.states}\n \
                Final States: {self.final_states}\n \
                Transitions: {self.transitions})"