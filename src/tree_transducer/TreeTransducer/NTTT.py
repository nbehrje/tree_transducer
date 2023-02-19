"""
Non-deterministic finite-state top-down tree transducer module
"""
from collections.abc import Iterable
from .TreeTransducer import TreeTransducer
from src.tree_transducer.Tree import Tree, VarLeaf
from itertools import product

class NTTT(TreeTransducer):
    """
    Non-deterministic finite-state bottom-up tree transducer class
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
            ValueError: The NTTT is not properly defined.
        """
        #Verify states
        if not self.final_states.issubset(self.states):
            raise ValueError("final_states must be a subset of states.")

        #Verify transitions
        transitions_states = set()
        transitions_in_symbols = set()
        transitions_out_symbols = set()
        for (k, v) in self.transitions.items():
            transitions_states.add(k[0])
            if k[1]:
                transitions_in_symbols.add(k[1])
            for tup in v:
                transitions_states.update(tup[0])  
                transitions_out_symbols.update(tup[1].get_values())
        if not transitions_states.issubset(self.states):
            raise ValueError(f"NTTT's transitions contain state(s) not present in its states: {transitions_states - self.states}")
        if not transitions_in_symbols.issubset(self.in_symbols):
            raise ValueError(f"NTTT's transitions contain input symbol(s) not present in its in_symbols: {transitions_in_symbols - self.in_symbols}")
        if not transitions_out_symbols.issubset(self.out_symbols):
            raise ValueError(f"NTTT's transitions contain output symbol(s) not present in its out_symbols: {transitions_out_symbols - self.out_symbols}")

    def transduce(self, tree: Tree) -> Tree:
        """
        Transduces the input Tree.

        Args: 
            tree: The Tree to be transduced.

        Returns:
            Tree: The set of new Trees made by applying the transduction to the input Tree
        """
        return set.union(*[self._transduce_helper(final_state, tree) for final_state in self.final_states])

    def _transduce_helper(self, state, in_tree: Tree) -> set:
        """
        Recursive helper for transduce()

        Args:
            state: The state of the tree.
            tree: The Tree to be transduced.

        Returns:
            set: The set of filled output Trees
        """
        num_in_children = len(in_tree.children)
        outs = self.transitions.get((state, in_tree.value, num_in_children), set())
        outs_e = self.transitions.get((state, "", 1), set())
        if outs == set() and outs_e == set():
            return set()
        filled = set()
        for (child_states, out_tree) in outs:
            child_trees = [self._transduce_helper(child_states[i], in_tree.children[i]) for i in range(num_in_children)]
            if set() in child_trees:
                continue
            child_combinations = list(product(*child_trees))
            out_trees = {out_tree.fill(child_combination) for child_combination in child_combinations}
            filled.update(out_trees)
        for (child_state, out_tree) in outs_e:
            child_trees = self._transduce_helper(next(iter(child_state)), in_tree)
            if child_trees == set():
                continue
            out_trees = {out_tree.fill((child_tree,)) for child_tree in child_trees}
            filled.update(out_trees)
        return filled

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