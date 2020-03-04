from openbiolink.namespace import Namespace
from openbiolink.nodeType import NodeType


class Node:
    def __init__(self, id: str, type: NodeType, namespace: Namespace, name=None):
        self.id = id
        self.type = type
        self.namespace = namespace
        self.name = name

    def __eq__(self, other):
        if isinstance(other, Node):
            return self.id == other.id
        return False

    def __hash__(self):
        return hash((self.id, self.type))

    def __iter__(self):
        return iter([self.resolved_id, self.type])

    @property
    def resolved_id(self):
        return self.namespace.resolve(self.id)
