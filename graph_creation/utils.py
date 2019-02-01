import pandas
from functools import reduce


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

def remove_bidir_edges_from_df (data):
    no_rows, _ = data.shape
    no_edges = int(no_rows / 2)
    temp_dic = {}
    cols=list(data)
    i = 0
    for row in data.itertuples():
        if len(cols)==3:
            other_row = row[2] + row[1] + str(row[3])
        elif len(cols)==2:
            other_row = row[2] + row[1]
        else:
            print(('WARNING: removing bidirectional edges requires 2 or 3 (incl score) columns but cols are '.join(cols))+ 'edges are not removed' )
            return data
        if len(cols)==3:
            if other_row not in temp_dic.keys():
                this_row = row[1] + row[2] + str(row[3])
                temp_dic[this_row] = [row[1], row[2], row[3]]
                i += 1
            if i == no_edges:
                break
        elif len(cols)==2:
            if other_row not in temp_dic.keys():
                this_row = row[1] + row[1]
                temp_dic[this_row] = [row[1], row[2]]
                i += 1
            if i == no_edges:
                break

    new_data = pandas.DataFrame.from_dict(temp_dic, columns=list(data), orient='index')
    return new_data


 # source: https://gist.github.com/wonderbeyond/d293e7a2af1de4873f2d757edd580288#file-rgetattr-py
def rgetattr(obj, attr, *args):
    def _getattr(obj, attr):
        return getattr(obj, attr, *args)
    return reduce(_getattr, [obj] + attr.split('.'))