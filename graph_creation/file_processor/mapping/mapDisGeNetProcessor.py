from graph_creation.metadata_infile.mapping.inMetaMapDisGeNet import InMetaMapDisGeNet

from graph_creation.Types.readerType import ReaderType
from graph_creation.file_processor.fileProcessor import FileProcessor
from graph_creation.Types.infileType import InfileType


class MapDisGeNetProcessor(FileProcessor):

    def __init__(self):
        self.use_cols = InMetaMapDisGeNet.USE_COLS
        super().__init__(self.use_cols, readerType=ReaderType.READER_MAP_DISGENET,
                         infileType=InfileType.IN_MAP_DISGENET, mapping_sep=InMetaMapDisGeNet.MAPPING_SEP)


    def individual_preprocessing(self, data):
        # making ids unique in DisGeNet mapping file for DO and OMIM (metadata_db_file:id)
        data.loc[data['voc'] == 'DO', 'code'] = 'DOID:' + data[data['voc'] == 'DO']['code']
        data = data[data['voc'] == 'DO']

        return data


