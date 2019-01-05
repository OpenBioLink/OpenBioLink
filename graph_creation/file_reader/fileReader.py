import gzip
import zipfile
from abc import ABC, abstractmethod


class FileReader (ABC):

    @staticmethod
    def open_file(in_path):
        path_parts = in_path.split('.')
        if (path_parts[-1] == "gz"):
            in_file = gzip.open(in_path, "rt", encoding="utf8")
        elif (path_parts[-1] == "zip"):
            zf = zipfile.ZipFile(in_path)
            in_file = zf.open(zf.namelist()[0])
        else:
            in_file = open(in_path)
        return in_file

    @abstractmethod
    def read_file(self):
        ...

