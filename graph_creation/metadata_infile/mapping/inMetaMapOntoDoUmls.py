from graph_creation.metadata_infile.infileMetadata import InfileMetadata
from graph_creation.infileType import InfileType
import graph_creation.constants.in_file.mapping.inMapOntoDoUmlsConstant as constant


class InMetaMapOntoDoUmls(InfileMetadata):

    def __init__(self, folder_path):
        super().__init__(csv_name=constant.CSV_NAME,
                         folder_path=folder_path,
                         infileType=InfileType.IN_MAP_ONTO_DO_UMLS)
