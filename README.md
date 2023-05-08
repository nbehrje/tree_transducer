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
