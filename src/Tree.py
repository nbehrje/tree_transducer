"""
Tree module
"""

class Tree:
    def __init__(self, node, children: list):
        self.node = node
        self.children = children

        self.validate_input()

    def validate_input(self):
        if self.node is None and len(self.children):
            raise ValueError("Tree with children has node type of None.")