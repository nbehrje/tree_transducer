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
* `transitions`: a dict containing the transitions with the key/value types depending on the directionality of the machine
  * bottom-up: each key is a tuple containing a tuple of states and a symbol, and each value is a set of states
  * top-down: each key is a tuple containing a state, a symbol, and an integer, and each value is a set of tuples of states
