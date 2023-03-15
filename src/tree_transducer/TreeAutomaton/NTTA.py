"""
Non-deterministic Top-down Tree Automaton Module
"""
from __future__ import annotations
from collections.abc import Iterable
from ..Tree import Tree
from .TreeAutomaton import TreeAutomaton
from itertools import product, chain
from collections import defaultdict
import copy

class NTTA(TreeAutomaton):
    """
    Non-deterministic top-down finite-state tree automaton
    """
    def __init__(self, states: Iterable, final_states: Iterable, symbols: Iterable, transitions: dict):
        """
        Creates a top-down tree automaton
        
        Args:
            states: An Iterable containing the set of states (Q)
            final_states: An Iterable containing the set of initial states (Q_i)
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
            for v_i in v:
                if not k[2] == len(v_i):
                    raise ValueError(f"Automaton's transition contains mismatched number of children: {k,v_i}")
                transitions_states.update(set(v_i))
            transitions_states.add(k[0])
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
        states = set.union(*[self.epsilon_closure[s] for s in self.final_states])
        return self._accept_helper(states, tree)

    def _accept_helper(self, states, tree: Tree) -> bool:
        """
        Recursive helper for accept()

        Args:
            state: The current possible states of the tree.
            tree: The candidate Tree.

        Returns:
            bool: True if some subtree is valid and False otherwise
        """
        keys = [(s, tree.value, len(tree.children)) for s in states]
        vals = set.union(*[self.transitions.get(key, set()) for key in keys])
        return vals and any([all(self._accept_helper(val[c],tree.children[c]) for c in range(len(tree.children)))] for val in vals)

    def get_epsilon_closure(self) -> dict:
        """
        Finds the epsilon closure for each states in the automaton

        Returns:
            dict: A dictionary with states as keys and sets of states as the values
        """
        e_closure = {s:set([s]) for s in self.states}

        for (k,v) in self.transitions.items():
            if k[1] == "":
                to_states = next(iter(v))[0]
                e_closure[k[0]].add(to_states)
        
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

    def union(self, other: NTTA) -> NTTA:
        """
        Returns the union of this top-down automaton and another top-down automaton.
        The states and transitions are the disjointed states and transitions of the input automata.
        An NTTA is always returned even if both input automata are deterministic.

        Returns:
            NTTA: the union of this top-down automaton and another top-down automaton
        """
        new_symbols = set(chain.from_iterable([self.symbols, other.symbols]))
        new_transitions = dict()
        new_final_states = {f"1_{s1}" for s1 in self.final_states}
        new_final_states.update({f"2_{s2}" for s2 in other.final_states})
        new_states = [f"1_{s1}" for s1 in self.states] + [f"2_{s2}" for s2 in other.states]
        new_transitions = {(f"1_{k[0]}",k[1],k[2]):{tuple(f"1_{s}" for s in vi) for vi in v} for k,v in self.transitions.items()} | \
            {(f"2_{k[0]}",k[1],k[2]):{tuple(f"2_{s}" for s in vi) for vi in v} for k,v in other.transitions.items()}
        return NTTA(new_states, new_final_states, new_symbols, new_transitions)

    def intersection(self, other: NTTA) -> NTTA:
        """
        Returns the intersection of this top-down automaton and another top-down automaton.
        The states and transitions are the products of the input automata.
        An NTTA is always returned even if both input automata are deterministic.

        Returns:
            NTTA: the intersection of this top-down automaton and another top-down automaton
        """
        state_pairs = [(s1, s2) for s1 in self.states for s2 in other.states]
        new_transitions = dict()
        for (s1,s2) in state_pairs:
            for self_key, self_val in self.transitions.items():
                if self_key[0] != s1:
                    continue
                symbol = self_key[1]
                rank = self_key[2]
                for other_key, other_val in other.transitions.items():
                    if other_key[1] != symbol or other_key[2] != rank:
                        continue
                    new_transitions[(f"{s1}_{s2}", symbol, rank)] = {tuple([f"{s_tup[i]}_{o_tup[i]}" for s_tup in self_val for o_tup in other_val for i in range(rank)])}
        new_states = [f"{s1}_{s2}" for s1 in self.states for s2 in other.states]
        new_final_states = [f"{s1}_{s2}" for s1 in self.states for s2 in other.states]
        new_symbols = self.symbols.union(other.symbols)
        return NTTA(new_states, new_final_states, new_symbols, new_transitions)

    def __eq__(self, other: object) -> bool:
        if isinstance(other, NTTA):
            return self.states == other.states and \
                    self.final_states == other.final_states and \
                    self.transitions == other.transitions
        return False

    def __str__(self) -> str:
        return f"NTTA(States: {self.states}\n \
                Final States: {self.final_states}\n \
                Transitions: {self.transitions})"

    def __repr__(self) -> str:
        return f"NTTA(States: {self.states}\n \
                Final States: {self.final_states}\n \
                Transitions: {self.transitions})"