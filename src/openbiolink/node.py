from openbiolink.nodeType import NodeType


class Node:
    def __init__(self, id: str, type: NodeType, name=""):
        self.id = id
        self.type = type

    def __eq__(self, other):
        if isinstance(other, Node):
            return self.id == other.id
        return False

    def __hash__(self):
        return hash((self.id, self.type))

    def __iter__(self):
        return iter([self.id, self.type])
