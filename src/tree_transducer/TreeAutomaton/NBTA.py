"""
Non-deterministic Bottom-up Tree Automaton Module
"""
from collections.abc import Iterable
from ..Tree import Tree
from .TreeAutomaton import TreeAutomaton
from itertools import product
from collections import defaultdict

class NBTA(TreeAutomaton):
    """
    Non-deterministic bottom-up finite-state tree automaton
    """

    def __init__(self, states: Iterable, final_states: Iterable, symbols: Iterable, transitions: dict):
        """
        Creates a bottom-up tree automaton
        
        Args:
            states: An Iterable containing the set of states (Q)
            final_states: An Iterable containing the set of final states (Q_f)
            symbols: An Iterable containing the set of symbols (F)
            transitions: A dict containing the transitions (Delta)

        Raises:
            ValueError: The NBTA is not properly defined.
        """
        super().__init__(states, final_states, symbols, transitions)
        self.epsilon_closure = self.get_epsilon_closure()

    def _validate_input(self):
        """
        Verifies that the arguments passed to init produce a well-defined automaton
        
        Raises:
            ValueError: The NBTA is not properly defined.
        """
        #Verify states
        if not self.final_states.issubset(self.states):
            raise ValueError("final_states must be a subset of states.")

        #Verify transitions
        transitions_states = set()
        transitions_symbols = set()
        for (k, v) in self.transitions.items():
            transitions_states.update(set(k[0]))
            transitions_states.update(v)
            if k[1]:
                transitions_symbols.add(k[1])
        if not transitions_states.issubset(self.states):
            raise ValueError(f"NBTA's transitions contain state(s) not present in its states: {transitions_states - self.states}")
        if not transitions_symbols.issubset(self.symbols):
            raise ValueError(f"NBTA's transitions contain symbol(s) not present in its symbols: {transitions_symbols - self.symbols}")

    def accepts(self, tree: Tree) -> bool:
        """
        Checks whether a tree is accepted by the automaton

        Args:
            tree: The candidate Tree.

        Returns:
            bool: True if the NBTA accepts the tree and False otherwise.
        """
        final_state = self._accept_helper(tree)
        for f in list(final_state):
            final_state.update(self.epsilon_closure.get(f))
        return final_state.intersection(self.final_states) != set()

    def _accept_helper(self, tree: Tree) -> set:
        """
        Recursive helper for accept()

        Args:
            tree: The candidate Tree.

        Returns:
            The set of possible states of the input Tree when processed by the automaton
        """
        child_states = tuple(self._accept_helper(c) for c in tree.children)
        child_possibilities = set(product(*child_states))
        states_read = [self.transitions.get((children, tree.value), set()) for children in child_possibilities] \
            + [self.transitions.get((children, ""), set()) for children in child_possibilities]
        states = states_read
        
        if states:
            return set.union(*states)
        return set()

    def get_epsilon_closure(self) -> dict:
        """
        Finds the epsilon closure for each states in the automaton

        Returns:
            dict: A dictionary with states as keys and sets of states as the values
        """
        e_closure = dict()

        for s in self.states:
            to_states = {v for v in self.transitions.get(((s,), ""), set())}
            to_states.add(s)
            e_closure[s] = to_states
            
        states = list(self.states)
        update = False
        i = 0
        l = len(states)
        while i < l:
            state = states[i]
            cur_closure = e_closure[state]
            for s in cur_closure:
                if not e_closure[s].issubset(cur_closure):
                    update = True
                    e_closure[state] = e_closure[state].union(e_closure[s])
            i += 1
            if i == l and update:
                i = 0
                update = False
        return e_closure