from openbiolink.graph_creation.metadata_edge.edgeMetadata import EdgeMetadata


class EdgeOntoMetadata(EdgeMetadata):
    def __init__(
        self,
        is_directional,
        edges_file_path,
        source,
        colindex1,
        colindex2,
        edgeType,
        node1_type,
        node1_namespace,
        node2_type,
        node2_namespace,
    ):
        super().__init__(
            is_directional=is_directional,
            edges_file_path=edges_file_path,
            source=source,
            colindex1=colindex1,
            colindex2=colindex2,
            edgeType=edgeType,
            node1_type=node1_type,
            node1_namespace=node1_namespace,
            node2_type=node2_type,
            node2_namespace=node2_namespace,
        )
