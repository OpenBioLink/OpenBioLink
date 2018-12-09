from nodeType import NodeType

class Node :
    def __init__(self, id: str, type : NodeType, name = "" ):
        self.id = id
        self.type = type
        self.name = name

    def __eq__(self, other):
        if isinstance(other, Node):
            return self.id == other.id
        return False

    def __hash__(self):
        return hash( (self.id, self.type))
