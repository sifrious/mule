import csv
from pprint import pprint


class Header:

    def __init__(self, row):
        try:
            if len(row) == 1:
                print(
                    f"attempting to split header with comma with row f{str(row)} @len {str(len(row))}")
                row = row[0].split(',')
        except Exception as e:
            print(f"couldn't split header {e}")
            pass
        finally:
            self.row = self.remove_spaces(row)

    def __repr__(self):
        return f"Header row: {self.row}"

    def remove_spaces(self, array):
        try:
            newArray = []
            for item in array:
                newArray.append(item.lower().replace(" ", "_"))
            return newArray
        except:
            return None


class Columns:

    def __init__(self, header, records):
        self.error = []
        self.header = header
        self.rows = records
        self.columns = self.form_columns()
        self.data = self.get()
        print(self.error)

    def form_columns(self):
        rows = [[] for i in range(len(self.header.row))]
        for row in self.rows:
            i = 0
            for cell in row:
                rows[i].append(cell)
                i += 1
        return rows

    def get(self):
        try:
            data = {}
            if self.columns != None:
                for key in self.header.row:
                    index = self.header.row.index(key)
                    data[key] = self.columns[index]
                return data
            else:
                self.error.append("couldn't form data from Null column input")
        except Exception as e:
            self.error.append(f"couldn't form data - {e}")
        return None


class CsvReader:

    def __init__(self, path):
        self.error = [None]
        self.path = path
        self.file = self.get()
        if self.file != None:
            self.header = Header(self.file[0])
            self.records = Columns(self.header, self.file[1:])
        else:
            print("couldn't find file")
            self.records = {"file": None}

    def getCommaSeperated(self):
        filestructure = []
        i = 0
        try:
            with open(self.path, "r", encoding="utf-16") as csv_file:
                freader = csv.reader(csv_file, delimiter=',')
                for row in freader:
                    rowArray = []
                    for cell in row:
                        rowArray.append(self.clean(str(cell)))
                    filestructure.append(rowArray)
                i += 0
        except Exception as e:
            print(f"Didn't save file - {e}")
        self.file = filestructure
        return filestructure

    def get(self):
        try:
            filestructure = []
            i = 0
            with open(self.path, "r", encoding="utf-16") as csv_file:
                freader = csv.reader(csv_file, delimiter='\t')
                for row in freader:
                    rowArray = []
                    if len(row) == 1:
                        return self.getCommaSeperated()
                    else:
                        for cell in row:
                            rowArray.append(self.clean(str(cell)))
                        filestructure.append(rowArray)
                i += 0
            return filestructure
        except FileNotFoundError:
            msg = f"Could not open {self.path}. File does not exist."
            self.error.append(msg)
        except:
            self.error.append(
                f"couldn't create csv file from path {self.path}")
        return None

    def get_column(self, column_name):
        # print("in get_column")
        # print(self.records.header.row)
        header = self.header.row
        if len(self.records.header.row) == 1:
            header = header[0].split(",")
            self.records.header.row = header
        if (column_name in self.records.header.row):
            # print(f"column_name is {column_name}")
            # pprint(self.records)
            # print(self.records.header)
            # print(self.records.header.row)
            return self.records.data[column_name]
        else:
            print(
                f"couldn't find {column_name} in {self.records.header.row}")

    @staticmethod
    def clean(raw_cell):
        cell = raw_cell
        return cell


if __name__ == '__main__':
    file = CsvReader("")
