# Tree Transducer library

This is a library for finite state tree machines in python.

## Trees
Trees are stored as a Tree object as defined in [Tree.py](src/tree_transducer/Tree.py). Its constructor takes two arguments: the value of the node and a list containing its children.

```
>>> Tree("a", [Tree("b"), Tree("c")])

a(b(),c())
```

### Tree Functions

#### is_leaf()
Returns whether the Tree is a leaf.

```
>>> Tree("a").is_leaf()

True
```

```
>>> Tree("a", [Tree("b")]).is_leaf()

False
```

#### term_yield()
Returns the list of leaves in the Tree.

```
>>> Tree("a", [Tree("b"), Tree("c")]).term_yield()

['b', 'c']
```

#### get_values()
Returns the set of values in the Tree.

```
>>> Tree("a", [Tree("b"), Tree("c")]).get_values()

{'a', 'c', 'b'}
```

### VarLeaf
VarLeaf is a subclass of Tree used for variable substitution in transducers. Its constructor takes an index that is used to select a Tree from a tuple provided to it. It does not store a value so `get_values()` will return `set()`.

```
>>> VarLeaf(0)

Var(0)
```

## Automata
Automata are represented as objects of one of four classes:
* [NBTA](src/tree_transducer/TreeAutomaton/NBTA.py) (nondeterministic bottom-up)
* [NTTA](src/tree_transducer/TreeAutomaton/NTTA.py) (nondeterministic top-down)
* [DBTA](src/tree_transducer/TreeAutomaton/DBTA.py) (deterministic bottom-up)
* [DTTA](src/tree_transducer/TreeAutomaton/DTTA.py) (deterministic top-down)

### Defining Automata
To create an automaton, pass four parameters:
* `states`: an Iterable containing the states
* `final_states`: an Iterable containing a subset of `states` as the accepting states (initial states in the case of top-down machines)
* `symbols`: an Iterable containing the symbols
* `transitions`: a dict containing the transitions with the key/value types depending on the directionality of the machine:
  * bottom-up: each key is a tuple containing a tuple of states and a symbol, and each value is a set of states
  * top-down: each key is a tuple containing a state, a symbol, and an integer, and each value is a set of tuples of states

Epsilon transitions can be created by using the empty string as a symbol in the transition's key.

This deterministic bottom-up automaton accepts trees that represent derivations for the context-free grammar {S -> a b; S -> a S b}:
```
>>> DBTA(
  states = {"qS", "qa", "qb"},
  final_states = {"qS"},
  symbols = {"S","a","b"},
  transitions = {
    (("qa","qb"), "S"): {"qS"},
    (("qa","qS","qb"), "S"): {"qS"},
    (tuple(), "a"): {"qa"},
    (tuple(), "b"): {"qb"}
  }
)

DBTA(States: {'qS', 'qa', 'qb'}
                 Final States: {'qS'}
                 Transitions: {(('qa', 'qb'), 'S'): {'qS'}, (('qa', 'qS', 'qb'), 'S'): {'qS'}, ((), 'a'): {'qa'}, ((), 'b'): {'qb'}})
```

This nondeterministic bottom-up automaton accepts trees that represent derivations for the context-free grammar {S -> a b; S -> a S b} or are leaves of a[] or b[]:
```
>>> NBTA(
  states = {"qS", "qa", "qb"},
  final_states = {"qS"},
  symbols = {"S","a","b"},
  transitions = {
    (("qa","qb"), "S"): {"qS"},
    (("qa","qS","qb"), "S"): {"qS"},
    (tuple(), "a"): {"qa", "qS"},
    (tuple(), "b"): {"qb", "qS"}
  }
)

NBTA(States: {'qb', 'qS', 'qa'}
                 Final States: {'qS'}
                 Transitions: {(('qa', 'qb'), 'S'): {'qS'}, (('qa', 'qS', 'qb'), 'S'): {'qS'}, ((), 'a'): {'qS', 'qa'}, ((), 'b'): {'qS', 'qb'}})
```

This deterministic top-down automaton accepts trees that represent derivations for the context-free grammar {S -> a b; S -> a S b}:
```
>>> DTTA(
  states = {"qS", "qa", "qb"},
  final_states = {"qS"},
  symbols = {"S","a","b"},
  transitions = {
    ("qS","S",2):{("qa","qb")},
    ("qS","S",3):{("qa","qS","qb")},
    ("qa","a",0):{tuple()},
    ("qb","b",0):{tuple()}
  }
)

DTTA(States: {'qb', 'qS', 'qa'}
                 Final States: {'qS'}
                 Transitions: {('qS', 'S', 2): {('qa', 'qb')}, ('qS', 'S', 3): {('qa', 'qS', 'qb')}, ('qa', 'a', 0): {()}, ('qb', 'b', 0): {()}})
```

This nondeterministic top-down automaton accepts trees that represent derivations for the context-free grammar {S -> a b; S -> b a}
```
>>> NTTA(
  states = {"qS", "qa", "qb"},
  final_states = {"qS"},
  symbols = {"S","a","b"},
  transitions = {
    ("qS","S",2):{("qa","qb"), ("qb", "qa")},
    ("qa","a",0):{tuple()},
    ("qb","b",0):{tuple()}
  }
)

NTTA(States: {'qb', 'qS', 'qa'}
                 Final States: {'qS'}
                 Transitions: {('qS', 'S', 2): {('qb', 'qa'), ('qa', 'qb')}, ('qa', 'a', 0): {()}, ('qb', 'b', 0): {()}})
```

### Checking Acceptance for Automata
To check whether an automaton accepts a tree, pass a Tree to the automaton's `accept()` method.
```
>>> automaton = NBTA(
  states = {"qS", "qa", "qb"},
  final_states = {"qS"},
  symbols = {"S","a","b"},
  transitions = {
    (("qa","qb"), "S"): {"qS"},
    (("qa","qS","qb"), "S"): {"qS"},
    (tuple(), "a"): {"qa", "qS"},
    (tuple(), "b"): {"qb", "qS"}
  }
)

>>> tree = Tree("S", [Tree("a"), Tree("b")])

>>> automaton.accepts(tree)

True

>>> tree = Tree("S", [Tree("b"), Tree("a")])
>>> automaton.accepts(tree)

False
```

### Closure Properties
The union of an automaton with another automaton of the same type can be created by passing that automaton to the first automaton's `union()` method.
The intersection of an automaton with another automaton of the same type can be created by passing that automaton to the first automaton's `intersection()` method.
NBTAs can be determinized with the `determinize()` method.
DBTAs can be minimized with the `minimize()` method.

### Creating from Context-Free Grammars
An NTTA can be created by passing a context-free grammar as a string to the class's `from_cfg()` method along with the start symbols and the terminal symbols.
Each rule must be on a separate line.

```
>>> NTTA.from_cfg("""
  S -> a b
  S -> a S b
""", starts={"S"}, terminals={"a","b"})

NTTA(States: {'qb', 'qS', 'qa'}
                 Final States: {'qS'}
                 Transitions: {('qS', 'S', 2): {('qa', 'qb')}, ('qS', 'S', 3): {('qa', 'qS', 'qb')}})
```

## Transducers
Automata are represented as objects of one of four classes:
* [NBTT](src/tree_transducer/TreeTransducer/NBTT.py) (nondeterministic bottom-up)
* [NTTT](src/tree_transducer/TreeTransducer/NTTT.py) (nondeterministic top-down)
* [DBTT](src/tree_transducer/TreeTransducer/DBTT.py) (deterministic bottom-up)
* [DTTT](src/tree_transducer/TreeTransducer/DTTT.py) (deterministic top-down)

### Defining Transducers
To create a transducer, pass four parameters:
* `states`: an Iterable containing the states
* `final_states`: an Iterable containing a subset of `states` as the accepting states (initial states in the case of top-down machines)
* `in_symbols`: an Iterable containing the symbols of the input
* `out_symbols`: an Iterable containing the symbols of the output
* `transitions`: a dict containing the transitions with the key/value types depending on the directionality of the machine:
  * bottom-up: each key is a tuple containing a tuple of states and a symbol, and each value is a list of tuples each containing a state and a Tree
  * top-down: each key is a tuple containing a state, a symbol, and an integer, and each value is a set of tuples each containing a tuple of states and a Tree

Epsilon transitions can be created by using the empty string as a symbol in the transition's key.

This deterministic bottom-up transducer reverses the order of each node's children:
```
>>> DBTT(["qS","qA","qB"],["qS"],["A","B","S"],["A","B","S"],{
         (("qA","qB"),"S"):[("qS",Tree("S", [VarLeaf(1), VarLeaf(0)]))],
         (("qA","qS","qB"),"S"):[("qS", Tree("S", [VarLeaf(2), VarLeaf(1), VarLeaf(0)]))],
                                 (tuple(), "A"):[("qA", Tree("A"))],
                                 (tuple(), "B"):[("qB", Tree("B"))]})
                                 
DBTT(States: {'qA', 'qB', 'qS'}
                 Final States: {'qS'}
                 Transitions: {(('qA', 'qB'), 'S'): [('qS', S(Var(1),Var(0)))], (('qA', 'qS', 'qB'), 'S'): [('qS', S(Var(2),Var(1),Var(0)))], ((), 'A'): [('qA', A())], ((), 'B'): [('qB', B())]})
```

This deterministic top-down transducer reverses the order of each node's children:
```
>>> DTTT(["qS","qA","qB"],["qS"],["A","B","S"],["A","B","S"],{
                        ("qS", "S", 2):{(("qA","qB"),Tree("S", [VarLeaf(1), VarLeaf(0)]))},
                        ("qS", "S", 3):{(("qA","qS","qB"),Tree("S", [VarLeaf(2), VarLeaf(1), VarLeaf(0)]))},
                        ("qB", "B", 0):{(tuple(),Tree("B"))},
                        ("qA", "A", 0):{(tuple(),Tree("A"))}
                        })
                        
DTTT(States: {'qA', 'qB', 'qS'}
                 Final States: {'qS'}
                 Transitions: {('qS', 'S', 2): {(('qA', 'qB'), S(Var(1),Var(0)))}, ('qS', 'S', 3): {(('qA', 'qS', 'qB'), S(Var(2),Var(1),Var(0)))}, ('qB', 'B', 0): {((), B())}, ('qA', 'A', 0): {((), A())}
```

This nondeterministic bottom-up transducer optionally reverses the order of each node's children:
```
>>> NBTT(["qS","qA","qB"],["qS"],["A","B","S"],["A","B","S"],{
              (("qA","qB"),"S"):[("qS",Tree("S", [VarLeaf(1), VarLeaf(0)])),("qS",Tree("S", [VarLeaf(0), VarLeaf(1)]))],
              (tuple(), "A"):[("qA", Tree("A"))],
              (tuple(), "B"):[("qB", Tree("B"))]})
              
NBTT(States: {'qA', 'qB', 'qS'}
                 Final States: {'qS'}
                 Transitions: {(('qA', 'qB'), 'S'): [('qS', S(Var(1),Var(0))), ('qS', S(Var(0),Var(1)))], ((), 'A'): [('qA', A())], ((), 'B'): [('qB', B())]})
```

This nondeterministic top-down transducer optionally reverses the order of each node's children:
```
>>> NTTT(["qS","qA","qB"],["qS"],["A","B","S"],["A","B","S"],{
                        ("qS", "S", 2):{(("qA","qB"),Tree("S", [VarLeaf(1), VarLeaf(0)])),(("qA","qB"),Tree("S", [VarLeaf(0), VarLeaf(1)]))},
                        ("qB", "B", 0):{(tuple(),Tree("B"))},
                        ("qA", "A", 0):{(tuple(),Tree("A"))}
                        })
                        
NTTT(States: {'qA', 'qB', 'qS'}
                 Final States: {'qS'}
                 Transitions: {('qS', 'S', 2): {(('qA', 'qB'), S(Var(1),Var(0))), (('qA', 'qB'), S(Var(0),Var(1)))}, ('qB', 'B', 0): {((), B())}, ('qA', 'A', 0): {((), A())}})
```

### Transforming with Transducers
To transform a tree with a transducer, pass a Tree to the transducer's `transduce()` function.
```
>>> transducer = NBTT(["qS","qA","qB"],["qS"],["A","B","S"],["A","B","S"],{
                  (("qA","qB"),"S"):[("qS",Tree("S", [VarLeaf(1), VarLeaf(0)])),("qS",Tree("S", [VarLeaf(0), VarLeaf(1)]))],
                  (tuple(), "A"):[("qA", Tree("A"))],
                  (tuple(), "B"):[("qB", Tree("B"))]})
>>> good_tree = Tree("S", [Tree("A"), Tree("B")])
>>> transducer.transduce(good_tree)

[S(B(),A()), S(A(),B())]

>>> bad_tree = Tree("S", [Tree("A"), Tree("A")])
>>> transducer.transduce(bad_tree)

[]
```

### Closure Properties
The union of a transducer with another transducer of the same type can be created by passing that transducer to the first transducer's `union()` method.
The intersection of a transducer with another automaton of the same type can be created by passing that transducer to the first transducer's `intersection()` method.
