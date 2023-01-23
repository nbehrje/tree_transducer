"""
Tree module
"""

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
        """Verifies that the arguments passed to init produce a well-defined tree
        
        Raises:
            ValueError: The tree's value has type None but the list of children is not empty.
        """
        if self.value is None and len(self.children):
            raise ValueError("Tree with children has value type of None.")

    def is_leaf(self) -> bool:
        """Returns whether the tree is a leaf
        
        Returns:
            bool: True if the tree is a leaf and False otherwise.
        """
        return not self.children

    def __str__(self) -> str:
        return f"{self.value}({','.join(str(c) for c in self.children)})"