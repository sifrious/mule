from .csv.reader import CsvReader as reader
from .csv.writer import CsvWriter as writer


class Configuration:

    def __init__(self, kwargs):
        self.custom = []
        self.read = False
        self.write = False
        for arg in kwargs:
            setattr(self, arg, kwargs["arg"])
            if kwargs["arg"] == 'read':
                self.read = True
            if kwargs["arg"] == 'write':
                self.write = True
            self.custom.append(arg)


class FileLibrary:

    def __init__(self, **kwargs):
        self.__name__ = "file library"
        self.config = None

    def configure(self, kwargs):
        self.config = Configuration(kwargs)

    def __repr__(self):
        msg = "filelib instance"
        for param in self:
            value = getattr(self, param)
            msg += f"  - {param}: {value}"
        return msg
