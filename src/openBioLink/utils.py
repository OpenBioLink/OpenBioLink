import csv
import logging
import os
import urllib.request
from functools import reduce

import pandas
import inspect

import evaluation.evalConfig as evalConst
import globalConfig as globConst


def get_leaf_subclasses(cls, class_set=None):
    """"
    Returns a set of all leaf subclasses (i.e. child classes that do not have child-classes on their own) of a specific class.
    If no subclasses exist, the class itself is returned.
    If cls=None, None is returned.

    Parameters
    ----------
       cls : class
           class of which leaf subclasses should be obtained
       class_set : set, optional
           this parameter is only meant for recursive calls
    Returns
    ----------
        class_set : set
            set of all leaf subclasses
    """
    if inspect.isclass(cls):
        if class_set is None:
            class_set = set()
        if len(cls.__subclasses__()) == 0:
            class_set.add(cls)
        else:
            class_set.union(x for c in cls.__subclasses__() for x in get_leaf_subclasses(c, class_set))
        return class_set
    return None


# def get_all_subclasses(self, cls):
#    return set(cls.__subclasses__()).union([x for c in cls.__subclasses__() for x in self.get_all_subclasses(c)])


def make_undir (data: pandas.DataFrame):
    """"
    Takes a DataFrame which contains directional edges with possible bidirectional edges and removes
    the bidirectional edges, so (A->B and B->A) becomes(A->B); further resets the index

    Parameters
    ----------
        data : pandas.DataFrame
            DataFrame with columns [id1, id2] or [id1, id2, score], containing directional edges
    Returns
    ----------
        new_data  : pandas.DataFrame
            DataFrame with columns [id1, id2] or [id1, id2, score] (depending on input), containing directional edges

    Examples
    ----------
    >>> d = pandas.DataFrame({'id1': list('abc'), 'id2': list('xcb')})
    >>> d
      id1 id2
    0   a   x
    1   b   c
    2   c   b
    >>> make_undir(d)
      id1 id2
    0   a   x
    1   b   c
    """

    temp_dic = {}
    cols=list(data)
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
        elif len(cols)==2:
            if other_row not in temp_dic.keys():
                this_row = row[1] + row[2]
                temp_dic[this_row] = [row[1], row[2]]

    new_data = pandas.DataFrame.from_dict(temp_dic, columns=list(data), orient='index').reset_index(drop=True)
    return new_data


 # source: https://gist.github.com/wonderbeyond/d293e7a2af1de4873f2d757edd580288#file-rgetattr-py
def rgetattr(obj, attr, *args):
    """"
        Parameters
        ----------
        Returns
        ----------
    """
    def _getattr(obj, attr):
        return getattr(obj, attr, *args)
    return reduce(_getattr, [obj] + attr.split('.'))


def db_mapping_file_to_dic(mapping_file, map_source_col, map_target_col, sep =';'):
    """"
    creates a dic out of a metadata_db_file mapping file {source_id : [target_ids]}
    if multiple rows with the same source id exist, the target-id-list holds multiple elements
    if one row holds multiple targets (multiple targets in one target cell), the resulting string is treated as one element

    Parameters
    ----------
        mapping_file : str
            absolute path to the mapping file; mapping file must be a csv-like with one source column and one target column
        map_source_col : int
            column index of source column
        map_target_col : int
            column index of target column
        sep : str, optional, default = ';'
            separator of the mapping csv file

    Returns
    ----------
        mapping : dict

    Examples
    -----------
    if the mapping file looks like this

    | source | target |
    - - - - - - - - - -
    | s1     | t1     |
    | s2     | t2     |
    | s1     | t3     |
    | s3     | t4, t5 |

    the resulting dictionary looks like this
    {
    's1' : ['t1', 't3']
    's2' : ['t2']
    's3' : ['t4, t5']
    }
    """

    mapping = None
    if (mapping_file is not None):
       mapping = {}
       with open(mapping_file, mode="r") as mapping_content1:
           reader = csv.reader(mapping_content1, delimiter=sep)

           for row in reader:
               if row[map_target_col]:
                   if row[map_source_col] in mapping:
                       mapping[row[map_source_col]].append(row[map_target_col])
                   else:
                       mapping[row[map_source_col]] = [row[map_target_col]]
           mapping_content1.close()
    return mapping


def cls_list_to_dic(clsList, keyAttr, condition = None):
    """"
        creates an attribute dic out of a class list {keyAttribute_value : [classes]}

        Parameters
        ----------
            clsList : list
                list of classes that should be grouped by certain attribute; classes must all contain the ´keyAttr´,
                e.g. be all subclasses of class X, where X.keyAttr exists
            keyAttr : str
                attribute, by which the classes shall be grouped by
            condition : lambda
                condition for class that must hold in order to be considered in the grouping

        Returns
        ----------
            dic : dict
                dictionary, where the value of the keyAttr is the key, and a list of classes,
                where the key attribute has this value, is the value, i.e. {keyAttribute_value : [classes]}
    """

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
    """"
    checks, whether an URL exists

        Parameters
        ----------
            url : str
                URL which should be checked
        Returns
        ----------
            bool
                True -> URL exists, False -> URL does not exist
    """
    opener = urllib.request.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0')]
    urllib.request.install_opener(opener)
    try:
        urllib.request.urlopen(url)
        return True
    except:
        return False


############# FROM TRAIN TEST SPLIT #################################

def get_diff(df1, df2, path=None):
    """"
    takes DataFrames with same column names and returns their differences
        Parameters
        ----------
            df1 : pandas.DataFram
                left DataFrame of the merge
            df2 : pandas.DataFrame
                right DataFrame of the join
            path : str, optional
                if provided, the differences are saved as csv files in the provided path

        Returns
        ----------
            left_only : pandas.DataFrame
                DataFrame containing rows that only appear in df1, but not df2
            right_only : pandas.DataFrame
                DataFrame containing rows that only appear in df2, but not df1
    """
    diff = pandas.merge(df1, df2, how='outer', indicator=True).loc[lambda x: x['_merge'] != 'both']
    left_only = diff.loc[lambda x: x._merge == 'left_only'].drop(['_merge'], axis=1)
    right_only = diff.loc[lambda x: x._merge == 'right_only'].drop(['_merge'], axis=1)
    if path:
        left_only.to_csv(os.path.join(path, 'diff_left_only.csv'), sep='\t', index=False, header=False)
        left_only.to_csv(os.path.join(path, 'diff_right_only.csv'), sep='\t', index=False, header=False)
    return left_only, right_only


def remove_reverse_edges(remain_set, remove_set):
    """"
    removes the reverse edges of the remove_set from the remain_set (return = remain-remove^-1)
        Parameters
        ----------
            remain_set : pandas.DataFrame
                DataFrame from which all reverse edges from remove_set shall be removed, columns #todo
            remove_set : pandas.DataFrame
                DataFrame holds all edges, whose reverse edges shall be removed in the remain_set, columns = #todo
        Returns
        ----------
            remain : pandas.DataFrame
                DataFame that contains no reverse edges from remove_set

    """
    #todo independent from globals
    if not remain_set.empty and not remove_set.empty:
        remove_set_copy = remove_set.copy()
        # changing columns of node1_id and node2_id
        cols_other_dir = list(remove_set_copy.columns)
        index_id1 = cols_other_dir.index(globConst.NODE1_ID_COL_NAME)
        index_id2 = cols_other_dir.index(globConst.NODE2_ID_COL_NAME)
        cols_other_dir[index_id1]= globConst.NODE2_ID_COL_NAME
        cols_other_dir[index_id2]= globConst.NODE1_ID_COL_NAME
        remove_set_copy.columns = cols_other_dir
        temp = pandas.merge(remain_set, remove_set_copy, how='left',
                            left_on=[globConst.NODE1_ID_COL_NAME, globConst.NODE2_ID_COL_NAME, globConst.EDGE_TYPE_COL_NAME],
                            right_on=[globConst.NODE1_ID_COL_NAME, globConst.NODE2_ID_COL_NAME, globConst.EDGE_TYPE_COL_NAME])
        temp.set_index(remain_set.index)
        # todo value should always be different? are there examples with diff qscore?
        remove = temp[(temp['value_x'] == temp['value_y'])] # if no match would be found in remove_set, value_y would be NaN
        remain = remain_set.drop(remove.index.values)
        return remain
    else:
        return remain_set


#nicetohave (2) more lvl transitivity
#def check_for_transitive_edges(df):
#    """"
#        Parameters
#        ----------
#        Returns
#        ----------
#    """
#    direct_child_dict = {}
#    for row in df[[globConst.NODE1_ID_COL_NAME, globConst.NODE2_ID_COL_NAME]].itertuples():
#        _, child, parent = row
#        if not parent in direct_child_dict.keys():
#            direct_child_dict[parent] = {child}
#        else:
#            direct_child_dict[parent].add(child)
#    # fix me check for cycles
#    all_children = set()
#    return (
#    [((child_set & direct_child_dict[c]), parent, c) for (parent, child_set) in direct_child_dict.items() for c in
#     child_set if c in direct_child_dict.keys() if (child_set & direct_child_dict[c])])
# def get_all_childs(self,direct_child_dict, current_parent, past_parents, all_children):
#    for child in direct_child_dict[current_parent]:
#        pass



def calc_corrupted_triples(pos_examples: pandas.DataFrame, nodes:pandas.DataFrame, filtered=True, path=None):
    """"
    calculates the corrupted triples (both corrupted heads as well as corrupted tails) for given true positive examples
        Parameters
        ----------
            pos_examples : pandas.DataFrame
                DataFrame with true examples of edges, columns = [node1_id, edgeType, node2_id]
            nodes : pandas.DataFrame
                DataFrame with all nodes of the graph columns = [node_id, node_type]
            filtered : bool, optional, default = True
                if filtered is true, filtered corrupted triples are created; that means, that only those corrupted triples,
                that do not exist in the graph, are kept
                if filtered is false, unfiltered corrupted triples are created; this means, that all corrupted triples are
                kept, even if they exist in the graph
            path : str, optional
                if provided, the corrupted triples are saved as csv files in the provided path; one file contains the corrupted heads, grouped by


        Returns
        ----------
    """
    nodeTypes = nodes[globConst.NODE_TYPE_COL_NAME].unique()
    nodes_dic = {nodeType: nodes[nodes[globConst.NODE_TYPE_COL_NAME] == nodeType][[globConst.ID_NODE_COL_NAME]] for nodeType in nodeTypes}

    corrupted_head_dict = {}
    corrupted_tail_dict = {}

    for quadruple in pos_examples.itertuples():
        _, head, relation,tail = quadruple
        head_nodes = nodes_dic[head.split('_')[0]][globConst.ID_NODE_COL_NAME]
        tail_nodes = nodes_dic[tail.split('_')[0]][globConst.ID_NODE_COL_NAME]
        all_corrupted_heads = pandas.DataFrame(columns=list(pos_examples))
        all_corrupted_tails = pandas.DataFrame(columns=list(pos_examples))
        #corrupting heads
        for i, node in enumerate(head_nodes):
            if not node == head:
                all_corrupted_heads.loc[i] = [node, relation, tail]
        #corrupting tails
        for i, node in enumerate(tail_nodes):
            if not node == tail:
                all_corrupted_tails.loc[i] = [head, relation, node]
        corrupted_head_dict[(head,relation,tail)] = _get_corrupted_examples(all_corrupted_heads, pos_examples, filtered)
        corrupted_tail_dict[(head,relation,tail)] = _get_corrupted_examples(all_corrupted_tails, pos_examples, filtered)

    [corrupted_head_dict[x].reset_index(inplace=True, drop=True) for x in corrupted_head_dict.keys()]
    [corrupted_tail_dict[x].reset_index(inplace=True, drop=True) for x in corrupted_tail_dict.keys()]

    if path:
        all_corrupted_head = _group_corrupted_examples(corrupted_head_dict,
                                                       [evalConst.CORRUPTED_GROUP_COL_NAME]+list(pos_examples)+[globConst.VALUE_COL_NAME])
        all_corrupted_tail = _group_corrupted_examples(corrupted_tail_dict,
                                                       [evalConst.CORRUPTED_GROUP_COL_NAME]+list(pos_examples)+[globConst.VALUE_COL_NAME])
        all_corrupted_head.to_csv(os.path.join(path, evalConst.CORRUPTED_HEADS_FILE_NAME), sep='\t', index=False, header=False)
        all_corrupted_tail.to_csv(os.path.join(path, evalConst.CORRUPTED_TAILS_FILE_NAME), sep='\t', index=False, header=False)

    return corrupted_head_dict, corrupted_tail_dict


def _get_corrupted_examples (corrupted_triples, pos_examples, filtered):
    """"
    Creates a dataset of corrupted triples according to the 'filtered' setting
        Parameters
        ----------
            corrupted_triples : pandas.DataFrame
                DataFrame with corrupted triples of one positive example, columns = [node1_id, edgeType, node2_id]
            pos_examples : pandas.DataFrame
                DataFrame with all edges that are present in the graph (= positive examples), columns = [node1_id, edgeType, node2_id]
            filtered : bool
                if true, filtered setting is applied; that means, that only those corrupted triples, that do not exist in the graph, are kept
                if false, unfiltered setting is applied; this means, that all corrupted triples are kept, even if they exist in the graph

        Returns
        ----------
            corrupted_triples : pandas.DataFrame
                DataFrame contains all valid corrupted triples, incl value (1 for positive example, 0 for negative example)
                columns = [node1_id, edgeType, node2_id, value]
    """
    corrupted_triples.reset_index(drop=True, inplace=True)
    true_neg_triples, _ = get_diff(corrupted_triples, pos_examples)
    if filtered:
        corrupted_triples = true_neg_triples
        corrupted_triples[globConst.VALUE_COL_NAME] = 0
    else:
        neg_indices = set(true_neg_triples.index)
        corrupted_triples[globConst.VALUE_COL_NAME] = 1
        corrupted_triples[globConst.VALUE_COL_NAME][neg_indices] = 0
    return corrupted_triples


def _group_corrupted_examples (corrupted_dict, col_names):
    """"
     Parameters
     ----------
        corrupted_dict : dictionary
            dictionary of all corrupted triples, triple (head_id, relation_id, tail_id) as key,
            pandas.DataFrame with columns [head, relation, tail, value]
        col_names : list
            list of column names for [group, head_id, relation_id, tail_id, value]
            where value determines whether the triple exists (1) or not (0) in the graph
     Returns
     ----------
        all_corrupted : pandas.DataFrame
            pandas DataFrame of all triples grouped by true positive triple
            columns are [group, head_id, relation_id, tail_id, value, tp]
            the true positive example (tp) is always the first on a group of corrupted triples
    """
    i = 0
    #col_names = col_names + ['tp']
    all_corrupted = pandas.DataFrame(columns=col_names)
    for key, df in sorted(corrupted_dict.items()):
        h, r, t = key
        true_example = pandas.DataFrame([[h, r, t]], columns=list(df))
        #true_example['tp'] = 1
        true_example[col_names[4]] = 1
        true_example[col_names[0]] = i
        #todo should there be an extra column for tp?
        #df['tp'] = 0
        df[col_names[0]] = i
        all_corrupted = all_corrupted.append(true_example)
        all_corrupted = all_corrupted.append(df)
        i += 1
    return all_corrupted


