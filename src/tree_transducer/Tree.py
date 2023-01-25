"""
Tree module
"""
from __future__ import annotations

class Tree:
    """
    Creates a Tree

    Args:
        value:
            The value of the data stored in the tree
        children:
            A list of the tree's children

    Raises:
        ValueError: value has None type and children is not empty
    """
    def __init__(self, value, children: list = []):
        self.value = value
        self.children = children

        self._validate_input()

    def _validate_input(self):
        """
        Verifies that the arguments passed to init produce a well-defined tree
        
        Raises:
            ValueError: The tree's value has type None but the list of children is not empty.
        """
        if self.value is None and len(self.children):
            raise ValueError("Tree with children has value type of None.")

    def is_leaf(self) -> bool:
        """
        Returns whether the tree is a leaf
        
        Returns:
            bool: True if the tree is a leaf and False otherwise.
        """
        return not self.children

    def term_yield(self) -> list:
        """
        Returns the terminal yield of the tree

        Returns:
            list: The terminal yield of the tree
        """
        if self.children:
            return sum([c.term_yield() for c in self.children],[])
        return [self.value]

    def fill(self, trees: tuple) -> Tree:
        self.children = [c.fill(trees) for c in self.children]
        return self

    def __str__(self) -> str:
        return f"{self.value}({','.join(str(c) for c in self.children)})"

    def __repr__(self) -> str:
        return f"{self.value}({','.join(str(c) for c in self.children)})"

    def __nonzero__(self) -> bool:
        return self.value is not None

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Tree):
            return self.value == other.value and self.children == other.children
        return False

class VarLeaf(Tree):
    def __init__(self, idx):
        self.idx = idx

    def fill(self, trees: tuple):
        if self.idx > len(trees):
            raise IndexError("VarLeaf index greater than length of filling trees")
        return trees[self.idx]

    def __str__(self) -> str:
        return f"Var({self.idx})"

    def __repr__(self) -> str:
        return f"Var({self.idx})"