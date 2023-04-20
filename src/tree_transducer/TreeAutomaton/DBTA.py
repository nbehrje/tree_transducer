"""
Deterministic Bottom-up Tree Automaton Module
"""
from __future__ import annotations
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

    def minimize(self) -> DBTA:
        """
        Minimizes this deterministic automaton.
        This automaton must be reduced first.

        Returns:
            DBTA: An automaton equivalent to this automaton with the lowest number of possible states.
        """
        rule_pairs = dict()
        eq_rel = dict()
        for q1 in self.states:
            for q2 in self.states:
                rule_pairs[(q1,q2)] = self._get_rule_pairs(q1,q2)
                if (q1 in self.final_states and q2 not in self.final_states) or \
                    (q1 not in self.final_states and q2 in self.final_states):
                        eq_rel[(q1,q2)] = False
                else:
                    eq_rel[(q1,q2)] = True

        while True:
            change = False
            for (q1, q2), eq in eq_rel.items():
                if eq:
                    equal = True
                    for (r1,r2) in rule_pairs[(q1,q2)]:
                        dest1 = next(iter(r1[1]))
                        dest2 = next(iter(r2[1]))
                        if not eq_rel[(dest1, dest2)]:
                            equal = False
                            break
                    if not equal:
                        eq_rel[(q1,q2)] = False
                        eq_rel[(q2,q1)] = False
                        change = True
            if not change:
                break        
        
        new_finals = set()

        eq_class = dict()
        for q1 in self.states:
            in_eq_class = False
            for q2 in eq_class:
                if eq_rel[(q1,q2)]:
                    eq_class[q1] = eq_class[q2]
                    in_eq_class = True
                    if q1 in self.final_states:
                        new_finals.add(q1)
                    break

            if not in_eq_class:
                new_eq_class = [q2 for q2 in self.states if eq_rel[(q1,q2)]]
                new_state = "_".join(new_eq_class)
                eq_class[q1] = new_state
                if q1 in self.final_states:
                    new_finals.add(new_state)

        new_transitions = {}
        for (key,val) in self.transitions.items():
            new_dest = eq_class[next(iter(val))]
            new_src = tuple([eq_class[q] for q in key[0]])
            new_transitions[(new_src, key[1])] = {new_dest}

        return DBTA(list(eq_class.values()), new_finals, self.symbols, new_transitions)

    def _get_rule_pairs(self,q1,q2) -> list:
        """
        Finds the pairs of transition rules that differ only by q1 in the first and q2 in the second.

        Args:
            q1: The first state
            q2: The second state

        Returns:
            list: A list of tuples each containing a (key,value) rule tuple that differs from the other rule tuple only by q1/q2
        """
        pairs = []
        for k1 in self.transitions:
            for k2 in self.transitions:
                if len(k1[0]) != len(k2[0]) or not q1 in k1[0] or not q2 in k2[0]:
                    continue
                diff_ct = 0
                q_idx = -1
                for i in range(len(k1[0])):
                    if k1[0] != k2[0]:
                        diff_ct += 1
                        q_idx = i
                    if diff_ct > 1:
                        break
                if (diff_ct == 0 and q1 == q2) or (diff_ct == 1 and k1[0][q_idx] == q1 and k2[0][q_idx] == q2):
                    pairs.append(((k1,self.transitions[k1]),(k2,self.transitions[k2])))
        return pairs