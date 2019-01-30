from graph_creation.Types.infileType import InfileType
from graph_creation.Types.readerType import ReaderType
from graph_creation.file_processor.fileProcessor import FileProcessor
from graph_creation.metadata_infile import InMetaEdgeStitchBindAct


class EdgeStitchBindActProcessor(FileProcessor):

    META_EDGE_CLASS = InMetaEdgeStitchBindAct

    def __init__(self):
        self.use_cols = self.META_EDGE_CLASS.USE_COLS
        super().__init__(self.use_cols, readerType=ReaderType.READER_EDGE_STITCH_ACTION,
                         infileType=InfileType.IN_EDGE_STITCH_BINDACT, mapping_sep=self.META_EDGE_CLASS.MAPPING_SEP)


    def individual_preprocessing(self, data):
        # only drug -> protein connections of single compounds (no merged)
        drug_protein = data.item_id_a.str.startswith('CIDs')
        mode = data['mode'] == 'binding'
        action_short = data['action']== 'ac'
        action_long = data['action'] == 'activation'
        data = data[drug_protein & mode & (action_long | action_short)]
        self.stitch_to_pubchem_id(data,self.use_cols.index('item_id_a'))
        return data