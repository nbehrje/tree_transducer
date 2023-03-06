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
        """
        Returns a tree filled by tuple of trees.
        Each VarLeaf subtree in the new tree is replaced with the tree from the tuple with the index of the VarLeaf.

        Args:
            trees: A Tuple containing the trees to be added to the tree

        Returns:
            Tree: The new Tree with VarLeaf subtrees replaced
        """
        return Tree(self.value, [c.fill(trees) for c in self.children])

    def get_values(self) -> set:
        """
        Returns a set of all the values within the tree

        Returns:
            set: the set of all the values within the tree
        """
        values = {self.value}.union(*[c.get_values() for c in self.children])
        return values

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

    def __hash__(self) -> int:
        return hash(self.__str__())

class VarLeaf(Tree):
    def __init__(self, idx):
        self.idx = idx

    def fill(self, trees: tuple):
        """
        Replaces a VarLeaf with an input tree with the same index as the VarLeaf

        Args:
            trees: A Tuple containing the tree to replace the VarLeaf

        Returns:
            Tree: the Tree in the tuple
        """
        if self.idx > len(trees):
            raise IndexError("VarLeaf index greater than length of filling trees")
        return trees[self.idx]

    def get_values(self) -> set:
        """
        Returns a set of all the values within the tree
        Returns an empty set because VarLeaf is not for storing values except the index

        Returns:
            set: the empty set
        """
        return set()

    def __eq__(self, other: object) -> bool:
        if isinstance(other, VarLeaf):
            return self.idx == other.idx
        return False

    def __str__(self) -> str:
        return f"Var({self.idx})"

    def __repr__(self) -> str:
        return f"Var({self.idx})"

    def __hash__(self) -> int:
        return hash(self.__str__())