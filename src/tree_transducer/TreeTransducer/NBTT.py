"""
Nondeterministic finite-state bottom-up tree transducer module
"""
from __future__ import annotations
from collections.abc import Iterable
from .TreeTransducer import TreeTransducer
from src.tree_transducer.Tree import Tree, VarLeaf
from itertools import product, chain
import copy

class NBTT(TreeTransducer):
    """
    Nondeterministic finite-state bottom-up tree transducer class
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
        super().__init__(states, final_states, in_symbols, out_symbols, transitions)
        self.epsilon_closure = self.get_epsilon_closure()

    def _validate_input(self):
        """
        Verifies that the arguments passed to init produce a well-defined transducer
        
        Raises:
            ValueError: The transducer is not properly defined.
        """
        #Verify states
        if not self.final_states.issubset(self.states):
            raise ValueError("final_states must be a subset of states.")

        #Verify transitions
        transitions_states = set()
        transitions_in_symbols = set()
        transitions_out_symbols = set()
        for (k, v) in self.transitions.items():
            transitions_states.update(set(k[0]))
            if k[1]:
                transitions_in_symbols.add(k[1])
            for t in v:
                transitions_states.add(t[0])
                transitions_out_symbols.update(t[1].get_values())
        if not transitions_states.issubset(self.states):
            raise ValueError(f"Transducer's transitions contain state(s) not present in its input states: {transitions_states - self.states}")
        if not transitions_in_symbols.issubset(self.in_symbols):
            raise ValueError(f"Transducer's transitions contain input symbol(s) not present in its input in_symbols: {transitions_in_symbols - self.in_symbols}")
        if not transitions_out_symbols.issubset(self.out_symbols):
            raise ValueError(f"Transducer's transitions contain output symbol(s) not present in its input out_symbols: {transitions_out_symbols - self.out_symbols}")

    def transduce(self, tree: Tree) -> Tree:
        """
        Transduces the input Tree.

        Args: 
            tree: The Tree to be transduced.

        Returns:
            Tree: A new Tree made by applying the transduction to the input Tree
        """
        outputs = self._transduce_helper(tree)
        outputs = set(outputs + [i for o in outputs for i in self._get_epsilon_closed_trees(o[0],o[1])])
        return list(map(lambda out: out[1], filter(lambda out : out[0] in self.final_states, outputs)))

    def _transduce_helper(self, tree: Tree):
        """
        Recursive helper for transduce()

        Args:
            tree: The Tree to be transduced.

        Returns:
            A tuple containing a state and an output tree that has that state
        """
        transitions_to = []
        if tree.is_leaf():
            transitions_to = self.transitions.get((tuple(), tree.value), [])
        else:
            children_poss = [self._transduce_helper(c) for c in tree.children]
            children_poss_epsilon = list(map(lambda children_tup_list: children_tup_list + [item for t in children_tup_list for item in self._get_epsilon_closed_trees(t[0], t[1])],children_poss))
            children_prod = list(product(*children_poss_epsilon))
            for tups in children_prod:
                child_states, child_trees = list(zip(*tups))
                output_tups = self.transitions.get((child_states, tree.value), [])
                for (parent_state, out_tree) in output_tups:
                    transitions_to.append((parent_state, out_tree.fill(child_trees)))
        return transitions_to

    def get_epsilon_closure(self) -> dict:
        """
        Finds the epsilon closure for each states in the automaton

        Returns:
            dict: A dictionary with states as keys and sets of states as the values
        """
        e_closure = dict()

        for s in self.states:
            to_states = {v[0] for v in self.transitions.get(((s,), ""), set())}
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
                if not all(st in cur_closure for st in e_closure[s]):
                    update = True
                    e_closure[state] = e_closure[state].union(e_closure[s])
            i += 1
            if i == l and update:
                i = 0
                update = False
        return e_closure

    def _get_epsilon_closed_trees(self, state, tree) -> list: 
        """
        Finds the output trees that can be generated without reading any symbols, not including the input tree.

        Args:
            state: The state of the Tree
            tree: The output tree

        Returns:
            list: The list of trees that can be made with only epsilon transitions, not including the input tree.
        """
        outs = []
        stack_out = self.transitions.get(((state,),""), []).copy()
        stack_tree = [tree] * len(stack_out)
        i = 0
        while i < len(stack_out):
            out_state, out_tree = stack_out[i][0],stack_out[i][1].fill((stack_tree[i],))
            outs.append((out_state, out_tree))
            next_outs = self.transitions.get(((out_state,),""), [])
            if next_outs:
                stack_out += next_outs
                stack_tree += [out_tree] * len(next_outs)
            i += 1
        return outs

    def union(self, other: NBTT) -> NBTT:
        """
        Returns the union of this bottom-up transducer and another bottom-up transducer.
        The states and transitions are the products of the input transducers.
        An NBTT is always returned even if both input transducers are deterministic.

        Returns:
            NBTT: the union of this bottom-up transducer and another bottom-up transducer
        """
        new_in_symbols = set(chain.from_iterable([self.in_symbols, other.in_symbols]))
        new_out_symbols = set(chain.from_iterable([self.out_symbols, other.out_symbols]))
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
                completed_transitions_self[(tuple(["%S%"] * r), symbol)] = {("%S%", VarLeaf(0))}
            other_diff = ranks[symbol] - other_ranks.get(symbol, set())
            for r in other_diff:
                completed_transitions_other[(tuple(["%S%"] * r), symbol)] = {("%S%", VarLeaf(0))}
        for k_s, v_s in completed_transitions_self.items():
            for k_o, v_o in completed_transitions_other.items():
                if not k_s[1] == k_o[1]:
                    continue
                if not len(k_s[0]) == len(k_o[0]):
                    continue
                new_children = tuple([f"{k_s[0][i]}_{k_o[0][i]}" for i in range(len(k_s[0]))])
                new_val = []
                new_states.update(new_children)
                for s1 in v_s:
                    for s2 in v_o:
                        s = f"{s1[0]}_{s2[0]}"
                        if s1[0] != "%S%":
                            new_val.append((s, s1[1]))
                        if s2[0] != "%S%":
                            new_val.append((s, s2[1]))
                        new_states.add(s)
                        if s1[0] in self.final_states or s2[0] in other.final_states:
                            new_final_states.add(s)
                new_transitions[(new_children, k_s[1])] = new_val
        return NBTT(new_states, new_final_states, new_in_symbols, new_out_symbols, new_transitions)

    def intersection(self, other: NBTT) -> NBTT:
        new_in_symbols = self.in_symbols.union(other.in_symbols)
        new_out_symbols = self.out_symbols.union(other.out_symbols)
        new_transitions = dict()
        new_final_states = {f"{s1}_{s2}" for s1 in self.final_states for s2 in other.final_states}
        completed_transitions_self = copy.deepcopy(self.transitions)
        completed_transitions_other = copy.deepcopy(other.transitions)
        new_states = {f"{s1}_{s2}" for s1 in self.states for s2 in other.states}
        for k_s, v_s in completed_transitions_self.items():
            for k_o, v_o in completed_transitions_other.items():
                if not k_s[1] == k_o[1]:
                    continue
                if not len(k_s[0]) == len(k_o[0]):
                    continue
                new_children = tuple([f"{k_s[0][i]}_{k_o[0][i]}" for i in range(len(k_s[0]))])
                new_val = []
                new_states.update(new_children)
                for s1 in v_s:
                    for s2 in v_o:
                        s = f"{s1[0]}_{s2[0]}"
                        new_val.append((s, s1[1]))
                        if (s, s2[1]) not in new_val:
                            new_val.append((s, s2[1]))
                        new_states.add(s)
                new_transitions[(new_children, k_s[1])] = new_val
        return NBTT(new_states, new_final_states, new_in_symbols, new_out_symbols, new_transitions)

    def __eq__(self, other: object) -> bool:
        if isinstance(other, NBTT):
            return self.states == other.states and \
                    self.final_states == other.final_states and \
                    self.transitions == other.transitions
        return False

    def __str__(self) -> str:
        return f"NBTT(States: {self.states}\n \
                Final States: {self.final_states}\n \
                Transitions: {self.transitions})"

    def __repr__(self) -> str:
        return f"NBTT(States: {self.states}\n \
                Final States: {self.final_states}\n \
                Transitions: {self.transitions})"