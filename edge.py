from edgeTypes import EdgeType

class Edge:
    def __init__(self, id1: str, type : EdgeType, id2: str, source: "", weight= None, qScore = None):
        self.id1 = id1
        self.type = type
        self.id2 = id2
        self.source = source
        self.weight = weight
        self.qScore = qScore

    def __eq__(self, other):
        if isinstance(other, Edge):
            return ((self.id1 == other.id1 and self.id2 == other.id2) or (self.id1 == other.id2 and self.id2 == other.id1))
        return False

    def __iter__(self):
        return iter([self.id1, self.type, self.id2, self.source, self.weight, self.qScore])
