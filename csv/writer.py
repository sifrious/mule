from pprint import pprint
import os


class Config:

    def __init__(self, source, **kwargs):
        self.errors = []
        self.path = kwargs["path"] if "path" in kwargs.keys() else ""
        self.source = source


class Source:

    allowed = ["default"]

    def __init__(self, input):
        self.keys = input.keys()
        self.data = self.setData(input)
        if self.data != None:
            self.path = self.setPath(input)
            self.config = self.configure(input)  # TODO replace configuration

    def setData(self, input):
        for source in Source.allowed:
            if source in input.keys():
                return input[source]
        else:
            return None

    def configure(self, input):
        if "default" in input.keys():
            # TODO replace configuration
            return Config("default", path=self.path)

    def setPath(self, input):
        if "path" in input.keys():
            return input["path"]
        else:
            return f"{os.getcwd()}/output"


class CsvWriter:

    def __init__(self, **kwargs):
        source = Source(kwargs)
        if source.data != None:
            self.data = source.data
            self.path = source.path
            self.write()

    def write(self):
        i = 0
        with open(self.path, mode='w') as output:
            for row in self.data:
                if row != []:
                    string_row = []
                    for cell in row:
                        cell = str(cell)
                        string_row.append(cell)
                    output.write(",".join(string_row)+"\n")
                    i += 1
