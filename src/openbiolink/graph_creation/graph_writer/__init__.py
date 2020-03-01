# -*- coding: utf-8 -*-

"""Graph writers."""

from typing import Mapping, Type

from openbiolink.graph_creation.graph_writer.base import GraphWriter
from openbiolink.graph_creation.graph_writer.bel_writer import GraphBELWriter
from openbiolink.graph_creation.graph_writer.graphRDFWriter import GraphRDFWriter
from openbiolink.graph_creation.graph_writer.graphTSVWriter import GraphTSVWriter
from openbiolink.graph_creation.graph_writer.pickle_writer import GraphPickleWriter

__all__ = [
    'GraphWriter',
    'GraphBELWriter',
    'GraphRDFWriter',
    'GraphTSVWriter',
    'GraphPickleWriter',
    'FORMATS',
]


def _get_subclasses_recursive(cls):
    for subclass in cls.__subclasses__():
        yield subclass
        yield from _get_subclasses_recursive(subclass)


FORMATS: Mapping[str, Type[GraphWriter]] = {
    cls.format_key: cls
    for cls in _get_subclasses_recursive(GraphWriter)
    if cls.format_key is not None
}
