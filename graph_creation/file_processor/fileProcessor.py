import pandas


class FileProcessor():

    def __init__(self, use_cols, readerType, infileType, mapping_sep = None):
        self.use_cols = use_cols
        self.readerType = readerType
        self.infileType = infileType
        self.mapping_sep = mapping_sep


    def flat_df(self, data):
        """creates a 'flat' df, i.e. no NAN columns and one relationship per row (a -> b,c) becomes (a -> b ; a -> c)"""
        drop_list = sorted(set(list(data))-set(self.use_cols))
        data = data.drop(drop_list, axis=1)
        data = data.dropna()
        if self.mapping_sep is not None:
            #todo performance
            temp = data[data[self.use_cols[0]].str.contains(self.mapping_sep)]
            for index, line in temp.iterrows():
                for alt in line[0].split(self.mapping_sep):
                    data = data.append(pandas.DataFrame([[alt.lstrip(), line[1]]], columns=self.use_cols))
            data = data[~data[self.use_cols[0]].str.contains(self.mapping_sep)]
            temp = data[data[self.use_cols[1]].str.contains(self.mapping_sep)]
            for index, line in temp.iterrows():
                for alt in line[1].split(self.mapping_sep):
                    data = data.append(pandas.DataFrame([[line[0], alt.lstrip()]], columns=self.use_cols))
            data = data[~data[self.use_cols[1]].str.contains(self.mapping_sep)]
        return data


    def individual_preprocessing(self, data):
        return data

    def individual_postprocessing(self, data):
        return data

    def stitch_to_pubchem_id(self, data, id_col):
        data[data.columns[id_col]] = data[data.columns[id_col]].str[4:].str.lstrip("0")
        return data



    def process(self, data):
        data = self.individual_preprocessing(data)
        data = data[self.use_cols]
        if self.mapping_sep is not None:
            data = self.flat_df(data)
        data = self.individual_postprocessing(data)
        return data



#class EdgeCdtPathProcessor(FileProcessor):
#    def __init__(self, data):
#        self.use_cols =  inEdgeCdtPathConstant.USE_COLS
#        super().__init__(data, self.use_cols, dbType=DbType.DB_EDGE_CDT_PATH, infileType=InfileType.IN_EDGE_CDT_PATH, mapping_sep=inEdgeCdtPathConstant.MAPPING_SEP)
#
#
#
#class EdgeDisGeNetProcessor(FileProcessor):
#    def __init__(self, data):
#        self.use_cols = inEdgeDisGeNetConstant.USE_COLS
#        super().__init__(data, self.use_cols, dbType=DbType.DB_EDGE_DISGENET, infileType=InfileType.IN_EDGE_DISGENET, mapping_sep=inEdgeDisGeNetConstant.MAPPING_SEP)
#
#
#
#class EdgeGoProcessor(FileProcessor):
#    def __init__(self, data):
#        self.use_cols = inEdgeGoConstant.USE_COLS
#        super().__init__(data, self.use_cols, dbType=DbType.DB_EDGE_GO, infileType=InfileType.IN_EDGE_GO, mapping_sep=inEdgeGoConstant.MAPPING_SEP)
#
#
#
#class EdgeHpaProcessor(FileProcessor):
#    def __init__(self, data):
#        self.use_cols = inEdgeHpaConstant.USE_COLS
#        super().__init__(data, self.use_cols, dbType=DbType.DB_EDGE_HPA, infileType=InfileType.IN_EDGE_HPA, mapping_sep=inEdgeHpaConstant.MAPPING_SEP)
#
#
#
#class EdgeHpoDisProcessor(FileProcessor):
#    def __init__(self, data):
#        self.use_cols = inEdgeHpoDisConstant.USE_COLS
#        super().__init__(data, self.use_cols, dbType=DbType.DB_EDGE_HPO_DIS, infileType=InfileType.IN_EDGE_HPO_DIS, mapping_sep=inEdgeHpoDisConstant.MAPPING_SEP)
#
#
#
#class EdgeHpoGeneProcessor(FileProcessor):
#    def __init__(self, data):
#        self.use_cols = inEdgeHpoGeneConstant.USE_COLS
#        super().__init__(data, self.use_cols, dbType=DbType.DB_EDGE_HPO_GENE, infileType=InfileType.IN_EDGE_HPO_GENE, mapping_sep=inEdgeHpoGeneConstant.MAPPING_SEP)
#
#
#
#class EdgeSiderIndProcessor(FileProcessor):
#    def __init__(self, data):
#        self.use_cols = inEdgeSiderIndConstant.USE_COLS
#        super().__init__(data, self.use_cols, dbType=DbType.DB_EDGE_SIDER_IND, infileType=InfileType.IN_EDGE_SIDER_IND, mapping_sep=inEdgeSiderIndConstant.MAPPING_SEP)
#
#
#
#class EdgeSiderSeProcessor(FileProcessor):
#    def __init__(self, data):
#        self.use_cols = inEdgeSiderSeConstant.USE_COLS
#        super().__init__(data, self.use_cols, dbType=DbType.DB_EDGE_SIDER_SE, infileType=InfileType.IN_EDGE_SIDER_SE, mapping_sep=inEdgeSiderSeConstant.MAPPING_SEP)
#
#
#
#class EdgeStitchProcessor(FileProcessor):
#    def __init__(self, data):
#        self.use_cols = inEdgeStitchConstant.USE_COLS
#        super().__init__(data, self.use_cols, dbType=DbType.DB_EDGE_STITCH, infileType=InfileType.IN_EDGE_STITCH, mapping_sep=inEdgeStitchConstant.MAPPING_SEP)
#
#
#
#class EdgeStringProcessor(FileProcessor):
#    def __init__(self, data):
#        self.use_cols = inEdgeStringConstant.USE_COLS
#        super().__init__(data, self.use_cols, dbType=DbType.DB_EDGE_STRING, infileType=InfileType.IN_EDGE_STRING, mapping_sep=inEdgeStringConstant.MAPPING_SEP)
#
#
#class mapDisGeNetProcessor(FileProcessor):
#    def __init__(self, data):
#        self.use_cols = inMapDisGeNetConstant.USE_COLS
#        super().__init__(data, self.use_cols, dbType=DbType.DB_MAP_DISGENET, infileType=InfileType.IN_MAP_DISGENET, mapping_sep=inMapDisGeNetConstant.MAPPING_SEP)