class DbFile:

    def __init__(self, edges_file_path, colindex1, colindex2, edgeType, node1_type, node2_type, colindex_qscore = None, cutoff_num = None, cutoff_txt = None,
                 mapping1_file = None, map1_sourceindex = None, map1_targetindex = None, db1_index = None, db1_name = None,
                 mapping2_file = None, map2_sourceindex = None, map2_targetindex = None, db2_index = None, db2_name = None):
            self.edges_file_path = edges_file_path
            self.colindex1= colindex1
            self.colindex2= colindex2
            self.edgeType= edgeType
            self.node1_type = node1_type
            self. node2_type = node2_type
            self.colindex_qscore = colindex_qscore
            self.cutoff_num = cutoff_num
            self.cutoff_txt= cutoff_txt
            self.mapping1_file = mapping1_file
            self.map1_sourceindex =map1_sourceindex
            self.map1_targetindex= map1_targetindex
            self.db1_index = db1_index
            self.db1_name= db1_name
            self.mapping2_file = mapping2_file
            self.map2_sourceindex =map2_sourceindex
            self.map2_targetindex =map2_targetindex
            self.db2_index = db2_index
            self.db2_name = db2_name
