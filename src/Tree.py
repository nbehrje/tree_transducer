"""
Tree module
"""

class Tree:
    """
    Creates a Tree

    Args:
        node:
            The value of the tree node
        children:
            A list of the tree's children

    Raises:
        ValueError: node has None type and children is not empty
    """
    def __init__(self, node, children: list):
        self.node = node
        self.children = children

        self.validate_input()

    def validate_input(self):
        if self.node is None and len(self.children):
            raise ValueError("Tree with children has node type of None.")