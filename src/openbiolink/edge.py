from openbiolink.edgeType import EdgeType
from openbiolink.node import Node


class Edge:
    def __init__(self, node1: Node, type: EdgeType, node2: Node, source: "", qscore=None, sourcedb=None):
        self.node1 = node1
        self.type = type
        self.node2 = node2
        self.source = source
        self.qscore = qscore
        self.sourcedb = sourcedb

    def __eq__(self, other):
        if isinstance(other, Edge):
            return (
                    self.type == other.type and self.node1.id == other.node1.id and self.node2.id == other.node2.id
            )  # todo only if directional
        return False

    def __hash__(self):
        return hash((self.node1.id, self.type, self.node2.id))

    def __iter__(self):
        return iter([self.node1.id, self.type, self.node2.id, self.qscore])

    def to_list(self, include_qscore):
        if include_qscore:
            return iter([self.resolve(self.node1), self.type,
                         self.resolve(self.node2), self.qscore, self.sourcedb])
        else:
            return iter([self.resolve(self.node1), self.type,
                         self.resolve(self.node2), "", self.sourcedb])

    def to_sub_rel_obj_list(self):
        return iter([self.node1.id, self.type, self.node2.id, self.sourcedb])

    @staticmethod
    def resolve(node):
        return node.namespace.resolve(node.id)
