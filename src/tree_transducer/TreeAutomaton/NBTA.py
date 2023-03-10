"""
Non-deterministic Bottom-up Tree Automaton Module
"""
from __future__ import annotations
from collections.abc import Iterable
from ..Tree import Tree
from .TreeAutomaton import TreeAutomaton
from itertools import product, chain
from collections import defaultdict
import copy

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
            ValueError: The automaton is not properly defined.
        """
        super().__init__(states, final_states, symbols, transitions)
        self.epsilon_closure = self.get_epsilon_closure()

    def _validate_input(self):
        """
        Verifies that the arguments passed to init produce a well-defined automaton
        
        Raises:
            ValueError: The automaton is not properly defined.
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
            raise ValueError(f"Automaton's transitions contain state(s) not present in its states: {transitions_states - self.states}")
        if not transitions_symbols.issubset(self.symbols):
            raise ValueError(f"Automaton's transitions contain symbol(s) not present in its symbols: {transitions_symbols - self.symbols}")

    def accepts(self, tree: Tree) -> bool:
        """
        Checks whether a tree is accepted by the automaton

        Args:
            tree: The candidate Tree.

        Returns:
            bool: True if the automaton accepts the tree and False otherwise.
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

    def union(self, other: NBTA) -> NBTA:
        """
        Returns the union of this bottom-up automaton and another bottom-up automaton.
        The states and transitions are the products of the input automata.
        An NBTA is always returned even if both input automata are deterministic.

        Returns:
            NBTA: the union of this bottom-up automaton and another bottom-up automaton
        """
        new_symbols = set(chain.from_iterable([self.symbols, other.symbols]))
        new_transitions = dict()
        new_final_states = {f"{s1}_{s2}" for s1 in self.final_states for s2 in other.states}
        new_final_states.update({f"{s1}_{s2}" for s1 in self.states for s2 in other.final_states})
        ranks = dict()
        self_ranks = dict()
        other_ranks = dict()
        completed_transitions_self = copy.deepcopy(self.transitions)
        completed_transitions_other = copy.deepcopy(other.transitions)
        new_states = {f"{s1}_{s2}" for s1 in self.states for s2 in other.states}
        for k in self.transitions.keys():
            r = ranks.get(k[1], set()).copy()
            r.add(len(k[0]))
            ranks[k[1]] = r
            self_r = self_ranks.get(k[1], set()).copy()
            self_r.add(len(k[0]))
            self_ranks[k[1]] = self_r
        for k in other.transitions.keys():
            r = ranks.get(k[1], set()).copy()
            r.add(len(k[0]))
            ranks[k[1]] = r
            other_r = other_ranks.get(k[1], set()).copy()
            other_r.add(len(k[0]))
            other_ranks[k[1]] = other_r
        for symbol in ranks:
            self_diff = ranks[symbol] - self_ranks.get(symbol, set())
            for r in self_diff:
                completed_transitions_self[(tuple(["%S%"] * r), symbol)] = {"%S%"}
            other_diff = ranks[symbol] - other_ranks.get(symbol, set())
            for r in other_diff:
                completed_transitions_other[(tuple(["%S%"] * r), symbol)] = {"%S%"}
        for k_s, v_s in completed_transitions_self.items():
            for k_o, v_o in completed_transitions_other.items():
                if not k_s[1] == k_o[1]:
                    continue
                if not len(k_s[0]) == len(k_o[0]):
                    continue
                new_children = tuple([f"{k_s[0][i]}_{k_o[0][i]}" for i in range(len(k_s[0]))])
                new_val = set()
                new_states.update(new_children)
                for s1 in v_s:
                    for s2 in v_o:
                        s = f"{s1}_{s2}"
                        new_val.add(s)
                        if s1 in self.final_states or s2 in other.final_states:
                            new_final_states.add(s)
                new_states.update(new_val)
                new_transitions[(new_children, k_s[1])] = new_val
        return NBTA(new_states, new_final_states, new_symbols, new_transitions)

    def __eq__(self, other: object) -> bool:
        if isinstance(other, NBTA):
            return self.states == other.states and \
                    self.final_states == other.final_states and \
                    self.transitions == other.transitions
        return False

    def __str__(self) -> str:
        return f"NBTA(States: {self.states}\n \
                Final States: {self.final_states}\n \
                Transitions: {self.transitions})"

    def __repr__(self) -> str:
        return f"NBTA(States: {self.states}\n \
                Final States: {self.final_states}\n \
                Transitions: {self.transitions})"