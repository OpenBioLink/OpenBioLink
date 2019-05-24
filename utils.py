import csv
import logging
import urllib.request
from functools import reduce

import pandas


############# FROM GRAPH CREATION #################################

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
            logging.warning(('removing bidirectional edges requires 2 or 3 (incl score) columns but cols are '.join(cols))+ 'edges are not removed' )
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


def db_mapping_file_to_dic(mapping_file, map_sourceindex, map_targetindex):
       """creates a dic out of a metadata_db_file mapping file {source_id : [target_ids]}"""
       if (mapping_file is not None):
           mapping = {}
           with open(mapping_file, mode="r") as mapping_content1:
               reader = csv.reader(mapping_content1, delimiter=";")

               for row in reader:
                   if row[map_sourceindex] in mapping:
                       mapping[row[map_sourceindex]].append(row[map_targetindex])
                   else:
                       mapping[row[map_sourceindex]] = [row[map_targetindex]]
               mapping_content1.close()
           return mapping


def cls_list_to_dic(clsList, keyAttr, condition = None):
   """creates a attribute dic out of a class list {keyAttribute : [classes]}"""
   if condition is None:
       condition = lambda a:True
   dic = {}
   for cls in clsList:
       if condition(cls):
           key = rgetattr(cls, keyAttr)
           if key in dic:
               dic[key].append(cls)
           elif key is not None:
               dic[key]= [cls]
   return dic


def file_exists(url):
    opener = urllib.request.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0')]
    urllib.request.install_opener(opener)
    try:
        urllib.request.urlopen(url)
        return True
    except:
        return False


############# FROM TRAIN TEST SPLIT #################################

def get_diff(df1, df2):
    diff = pandas.merge(df1, df2, how='outer', indicator=True).loc[lambda x: x['_merge'] != 'both']
    left_only = diff.loc[lambda x: x._merge == 'left_only'].drop(['_merge'], axis=1)
    right_only = diff.loc[lambda x: x._merge == 'left_only'].drop(['_merge'], axis=1)
    # fixme naming convention for output to ensure same output
    return left_only, right_only


def remove_bidir_edges(remain_set, remove_set):
    remove_set_copy = remove_set.copy()
    cols_other_dir = list(remove_set_copy.columns)
    index_id1 = cols_other_dir.index('id1')
    index_id2 = cols_other_dir.index('id2')
    cols_other_dir[index_id1]= 'id2'
    cols_other_dir[index_id2]= 'id1'
    remove_set_copy.columns = cols_other_dir
    temp = pandas.merge(remain_set, remove_set_copy, how='left', left_on=['id1', 'id2', 'edgeType'],
                        right_on=['id1', 'id2', 'edgeType'])
    temp.set_index(remain_set.index)
    # todo value should always be different? are there examples with diff qscore?
    remove = temp[(temp['value_x'] == temp['value_y'])]
    remain = remain_set.drop(remove.index.values)
    return remain


def check_for_transitive_edges(df):
    direct_child_dict = {}
    for row in df[['id1', 'id2']].itertuples():
        _, child, parent = row
        if not parent in direct_child_dict.keys():
            direct_child_dict[parent] = {child}
        else:
            direct_child_dict[parent].add(child)
    # fixme check for cycles
    all_children = set()
    return (
    [((child_set & direct_child_dict[c]), parent, c) for (parent, child_set) in direct_child_dict.items() for c in
     child_set if c in direct_child_dict.keys() if (child_set & direct_child_dict[c])])

# def get_all_childs(self,direct_child_dict, current_parent, past_parents, all_children):
#    for child in direct_child_dict[current_parent]:
#        pass
# fixme continue here (more lvl transitivity



