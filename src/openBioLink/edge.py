from openbiolink.edgeType import EdgeType


class Edge:
    def __init__(self, id1: str, type: EdgeType, id2: str, source: "", qScore=None):
        self.id1 = id1
        self.type = type
        self.id2 = id2
        self.source = source
        self.qScore = qScore

    def __eq__(self, other):
        if isinstance(other, Edge):
            return self.type == other.type and self.id1 == other.id1 and self.id2 == other.id2  # todo only if directional
        return False

    def __hash__(self):
        return hash((self.id1, self.type, self.id2))

    def __iter__(self):
        return iter([self.id1, self.type, self.id2, self.qScore])

    def to_sub_rel_obj_list(self):
        return iter([self.id1, self.type, self.id2])
