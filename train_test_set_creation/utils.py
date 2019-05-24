import pandas

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


