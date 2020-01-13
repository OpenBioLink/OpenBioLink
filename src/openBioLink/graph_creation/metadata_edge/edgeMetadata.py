class EdgeMetadata:
    MAP1_META_CLASS = None
    MAP2_META_CLASS = None
    MAP1_ALT_ID_META_CLASS = None
    MAP2_ALT_ID_META_CLASS = None

    def __init__(self, is_directional, edges_file_path, colindex1, colindex2, edgeType, node1_type, node2_type,
                 colindex_qscore=None, cutoff_num=None, cutoff_txt=None,
                 mapping1_file=None, map1_sourceindex=None, map1_targetindex=None,
                 altid_mapping1_file=None, altid_map1_sourceindex=None, altid_map1_targetindex=None,
                 mapping2_file=None, map2_sourceindex=None, map2_targetindex=None,
                 altid_mapping2_file=None, altid_map2_sourceindex=None, altid_map2_targetindex=None
                 ):
        self.is_directional = is_directional
        self.edges_file_path = edges_file_path
        self.colindex1 = colindex1
        self.colindex2 = colindex2
        self.edgeType = edgeType
        self.node1_type = node1_type
        self.node2_type = node2_type
        self.colindex_qscore = colindex_qscore
        self.cutoff_num = cutoff_num
        self.cutoff_txt = cutoff_txt

        self.mapping1_file = mapping1_file
        self.map1_sourceindex = map1_sourceindex
        self.map1_targetindex = map1_targetindex

        self.altid_mapping1_file = altid_mapping1_file
        self.altid_map1_sourceindex = altid_map1_sourceindex
        self.altid_map1_targetindex = altid_map1_targetindex

        self.mapping2_file = mapping2_file
        self.map2_sourceindex = map2_sourceindex
        self.map2_targetindex = map2_targetindex

        self.altid_mapping2_file = altid_mapping2_file
        self.altid_map2_sourceindex = altid_map2_sourceindex
        self.altid_map2_targetindex = altid_map2_targetindex
