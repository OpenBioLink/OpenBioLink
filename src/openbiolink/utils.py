import csv
import inspect
import logging
import os
import sys
import urllib.request
from functools import reduce

import numpy as np
import pandas

from openbiolink import globalConfig as globConst
from openbiolink.edgeType import EdgeType

pandas.set_option(
    "mode.chained_assignment", None
)  # Suppression of SettingWithCopy Warning see https://www.dataquest.io/blog/settingwithcopywarning/


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


def make_undir(data: pandas.DataFrame):
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
    cols = list(data)
    for row in data.itertuples():
        if len(cols) == 3:
            other_row = row[2] + row[1] + str(row[3])
        elif len(cols) == 2:
            other_row = row[2] + row[1]
        else:
            logging.warning(
                ("removing bidirectional edges requires 2 or 3 (incl score) columns but cols are ".join(cols))
                + "edges are not removed"
            )
            return data
        if len(cols) == 3:
            if other_row not in temp_dic.keys():
                this_row = row[1] + row[2] + str(row[3])
                temp_dic[this_row] = [row[1], row[2], row[3]]
        elif len(cols) == 2:
            if other_row not in temp_dic.keys():
                this_row = row[1] + row[2]
                temp_dic[this_row] = [row[1], row[2]]

    new_data = pandas.DataFrame.from_dict(temp_dic, columns=list(data), orient="index").reset_index(drop=True)
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

    return reduce(_getattr, [obj] + attr.split("."))


def db_mapping_file_to_dic(mapping_file, map_source_col, map_target_col, sep=";"):
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
    if mapping_file is not None:
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


def cls_list_to_dic(clsList, keyAttr, condition=None):
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
        condition = lambda a: True
    dic = {}
    for cls in clsList:
        if condition(cls):
            key = rgetattr(cls, keyAttr)
            if key in dic:
                dic[key].append(cls)
            elif key is not None:
                dic[key] = [cls]
    return dic


def url_exists(url):
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
    opener.addheaders = [("User-agent", "Mozilla/5.0")]
    urllib.request.install_opener(opener)
    try:
        urllib.request.urlopen(url)
        return True
    except:
        return False


############# FROM TRAIN TEST SPLIT #################################


def get_diff(df1, df2, ignore_qscore=False, path=None):
    """"
    takes DataFrames with same column names and returns their differences
        Parameters
        ----------
            df1 : pandas.DataFrame
                left DataFrame of the merge
            df2 : pandas.DataFrame
                right DataFrame of the join
            ignore_qscore : bool
                whether the quality score columns should be ignored when merging the data frames
            path : str, optional
                if provided, the differences are saved as csv files in the provided path

        Returns
        ----------
            left_only : pandas.DataFrame
                DataFrame containing rows that only appear in df1, but not df2
            right_only : pandas.DataFrame
                DataFrame containing rows that only appear in df2, but not df1
    """
    df1["id1"] = df1["id1"].astype(str)
    df1["id2"] = df1["id2"].astype(str)
    df1["edgeType"] = df1["edgeType"].astype(str)
    df2["id1"] = df2["id1"].astype(str)
    df2["id2"] = df2["id2"].astype(str)
    df2["edgeType"] = df2["edgeType"].astype(str)
    all_cols = globConst.COL_NAMES_SAMPLES
    all_cols_without_source = [
        globConst.NODE1_ID_COL_NAME,
        globConst.EDGE_TYPE_COL_NAME,
        globConst.NODE2_ID_COL_NAME,
        globConst.QSCORE_COL_NAME,
        globConst.VALUE_COL_NAME
    ]

    if ignore_qscore:
        cols = globConst.COL_NAMES_TRIPLES + [globConst.VALUE_COL_NAME]
        diff = pandas.merge(df1, df2, how="outer", left_on=cols, right_on=cols, indicator=True).loc[
            lambda x: x["_merge"] != "both"
        ]
        left_only = diff.loc[lambda x: x._merge == "left_only"]
        left_only[globConst.SOURCE_COL_NAME] = left_only[globConst.SOURCE_COL_NAME + "_x"]
        left_only[globConst.QSCORE_COL_NAME] = left_only[globConst.QSCORE_COL_NAME + "_x"]
        left_only = left_only[all_cols]
        left_only.drop_duplicates(subset=all_cols_without_source, inplace=True, keep=False)
        right_only = diff.loc[lambda x: x._merge == "right_only"]
        right_only[globConst.QSCORE_COL_NAME] = right_only[globConst.QSCORE_COL_NAME + "_y"]
        right_only[globConst.SOURCE_COL_NAME] = right_only[globConst.SOURCE_COL_NAME + "_y"]
        right_only = right_only[all_cols]
        right_only.drop_duplicates(subset=all_cols_without_source, inplace=True, keep=False)
    elif set(all_cols) == set(df1.columns.values) and set(all_cols) == set(df2.columns.values):
        diff = pandas.merge(
            df1,
            df2,
            how="outer",
            left_on=all_cols_without_source,
            right_on=all_cols_without_source,
            indicator=True
        ).loc[lambda x: x["_merge"] != "both"]
        left_only = diff.loc[lambda x: x._merge == "left_only"]
        left_only[globConst.SOURCE_COL_NAME] = left_only[globConst.SOURCE_COL_NAME + "_x"]
        left_only = left_only[all_cols]
        right_only = diff.loc[lambda x: x._merge == "right_only"]
        right_only[globConst.SOURCE_COL_NAME] = right_only[globConst.SOURCE_COL_NAME + "_x"]
        right_only = right_only[all_cols]
    else:
        diff = pandas.merge(df1, df2, how="outer", indicator=True).loc[lambda x: x["_merge"] != "both"]
        left_only = diff.loc[lambda x: x._merge == "left_only"].drop(["_merge"], axis=1)
        right_only = diff.loc[lambda x: x._merge == "right_only"].drop(["_merge"], axis=1)
    if path:
        left_only.to_csv(os.path.join(path, "diff_left_only.csv"), sep="\t", index=False, header=False)
        right_only.to_csv(os.path.join(path, "diff_right_only.csv"), sep="\t", index=False, header=False)
    return left_only, right_only


def remove_inconsistent_edges(df: pandas.DataFrame):
    """ removes edges that contain inconsistent information i.e. when an edge is present both as positive and negative example"""
    return df.drop_duplicates(
        subset=[globConst.NODE1_ID_COL_NAME, globConst.NODE2_ID_COL_NAME, globConst.EDGE_TYPE_COL_NAME], keep=False
    )


def remove_parent_duplicates_and_reverses(remain_set, remove_set):
    if not remain_set.empty and not remove_set.empty:
        remove_set_copy = remove_set.copy()
        remove_set_copy[globConst.EDGE_TYPE_COL_NAME] = remove_set_copy[globConst.EDGE_TYPE_COL_NAME].apply(
            lambda x: EdgeType[x].get_parent() if type(x) == str else x.get_parent()
        )
        remove_set_copy.drop_duplicates(
            inplace=True,
            subset=[globConst.NODE1_ID_COL_NAME, globConst.NODE2_ID_COL_NAME, globConst.EDGE_TYPE_COL_NAME],
        )
        remain_set, _ = get_diff(remain_set, remove_set_copy, ignore_qscore=True)
        remain_set.drop_duplicates(
            inplace=True,
            subset=[globConst.NODE1_ID_COL_NAME, globConst.NODE2_ID_COL_NAME, globConst.EDGE_TYPE_COL_NAME],
        )
        remain_set = remove_reverse_edges(remain_set, remove_set_copy)
    return remain_set
    # testme


def remove_reverse_edges(remain_set, remove_set):
    """"
    removes the reverse edges of the remove_set from the remain_set (return = remain-remove^-1), sets may not contain duplicates!
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
    # todo independent from globals
    if not remain_set.empty and not remove_set.empty:
        remain_set.reset_index(drop=True, inplace=True)
        remove_set.reset_index(drop=True, inplace=True)
        remove_set_copy = remove_set.copy()
        # changing columns of node1_id and node2_id
        cols_other_dir = list(remove_set_copy.columns)
        index_id1 = cols_other_dir.index(globConst.NODE1_ID_COL_NAME)
        index_id2 = cols_other_dir.index(globConst.NODE2_ID_COL_NAME)
        cols_other_dir[index_id1] = globConst.NODE2_ID_COL_NAME
        cols_other_dir[index_id2] = globConst.NODE1_ID_COL_NAME
        remove_set_copy.columns = cols_other_dir
        temp = pandas.merge(
            remain_set,
            remove_set_copy,
            how="left",
            left_on=[globConst.NODE1_ID_COL_NAME, globConst.NODE2_ID_COL_NAME, globConst.EDGE_TYPE_COL_NAME],
            right_on=[globConst.NODE1_ID_COL_NAME, globConst.NODE2_ID_COL_NAME, globConst.EDGE_TYPE_COL_NAME],
        )
        temp.set_index(remain_set.index)
        temp.drop_duplicates(inplace=True)

        # todo value should always be different? are there examples with diff qscore?
        remove = temp[
            (temp["value_x"] == temp["value_y"])
        ]  # if no match would be found in remove_set, value_y would be NaN
        remain = remain_set.drop(remove.index.values)
        return remain
    else:
        return remain_set


# nicetohave (2) more lvl transitivity
# def check_for_transitive_edges(df):
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
