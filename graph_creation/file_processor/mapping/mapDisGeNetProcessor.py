import os
import graph_creation.constants.globalConstant as glob
from graph_creation.file_processor.fileProcessor import FileProcessor
from graph_creation.dbType import DbType
from graph_creation.infileType import InfileType
import graph_creation.constants.in_file.mapping.inMapDisGeNetConstant as constant
import pandas


class MapDisGeNetProcessor(FileProcessor):

    def __init__(self):
        self.use_cols = constant.USE_COLS
        super().__init__(self.use_cols, dbType=DbType.DB_MAP_DISGENET, infileType=InfileType.IN_MAP_DISGENET, mapping_sep=constant.MAPPING_SEP)


    def individual_preprocessing(self, data):
        # making ids unique in DisGeNet mapping file for DO and OMIM (metadata_db_file:id)
        data.loc[data['voc'] == 'DO', 'code'] = 'DOID:' + data[data['voc'] == 'DO']['code'] #fixme wäh strings
        data = data[data['voc'] == 'DO']

        return data


