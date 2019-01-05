from graph_creation.metadata_infile.infileMetadata import InfileMetadata
from graph_creation.infileType import InfileType
import graph_creation.constants.in_file.onto.inOntoGoConstant as constant


class InMetaOntoGo(InfileMetadata):

    def __init__(self, folder_path):
        super().__init__(csv_name=constant.CSV_NAME,
                         folder_path=folder_path,
                         infileType=InfileType.IN_ONTO_GO)
