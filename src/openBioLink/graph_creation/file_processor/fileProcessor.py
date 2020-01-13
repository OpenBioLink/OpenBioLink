import logging

import pandas


class FileProcessor():

    def __init__(self, use_cols, readerType, infileType, mapping_sep=None):
        self.use_cols = use_cols
        self.readerType = readerType
        self.infileType = infileType
        self.mapping_sep = mapping_sep

    def flat_df(self, data):
        """creates a 'flat' df, i.e. no NAN columns and one relationship per row (a -> b,c) becomes (a -> b ; a -> c) and (a,b -> c) becomes (a->c; b->c)"""
        drop_list = sorted(set(list(data)) - set(self.use_cols))
        data = data.drop(drop_list, axis=1)
        data = data.dropna()
        if self.mapping_sep is not None and not data.empty:
            temp = data[data[self.use_cols[0]].str.contains(self.mapping_sep, regex=False)]
            for row in temp.itertuples():
                for alt in row[1].split(self.mapping_sep):
                    data = data.append(pandas.DataFrame([[alt.lstrip(), row[2]]], columns=self.use_cols))
            data = data[~data[self.use_cols[0]].str.contains(self.mapping_sep, regex=False)]
            temp = data[data[self.use_cols[1]].str.contains(self.mapping_sep, regex=False)]
            for row in temp.itertuples():
                for alt in row[2].split(self.mapping_sep):
                    data = data.append(pandas.DataFrame([[row[1], alt.lstrip()]], columns=self.use_cols))
            data = data[~data[self.use_cols[1]].str.contains(self.mapping_sep, regex=False)]
        return data

    def individual_preprocessing(self, data):
        return data

    def individual_postprocessing(self, data):
        return data

    def process(self, data):
        data = self.individual_preprocessing(data)
        data = data[self.use_cols]
        if self.mapping_sep is not None:
            data = self.flat_df(data)
        data = self.individual_postprocessing(data)
        rows, _ = data.shape
        if rows == 0:
            logging.warning('WARNING: The preprocessing of this processor removed all data.')
        return data

    @staticmethod
    def stitch_to_pubchem_id(data, id_col):
        data.iloc[:, id_col] = data[data.columns[id_col]].str[4:].astype(int)
        return data
