def get_leaf_subclasses(cls, classSet=None):
    if classSet is None:
        classSet = set()
    if len(cls.__subclasses__()) == 0:
        classSet.add(cls)
    else:
        classSet.union(x for c in cls.__subclasses__() for x in get_leaf_subclasses(c, classSet))
    return classSet

 #def get_all_subclasses(self, cls):
    #    return set(cls.__subclasses__()).union([x for c in cls.__subclasses__() for x in self.get_all_subclasses(c)])
