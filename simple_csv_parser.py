"""
Alexander Bürow - 13 October 2023

License: GPL3
"""

class FileParser:
    def __init__(self, filename):
        self._filename = filename

    def csv_reader(self) -> dict[str, list[str, ...]]:
        return self.csv_reader_custom(sep=",")

    def csv_reader_custom(self, sep: str):
        csv_dict = dict()
        keys = list()
        with open(self._filename, "r") as csv:
            for index_file, line in enumerate(csv):
                if index_file == 0:
                    for key in line.split(sep):
                        csv_dict[key.strip()] = None
                        keys.append(key.strip())
                else:
                    values = line.split(sep)
                    for index_line, value in enumerate(values):
                        if csv_dict[keys[index_line]] is None:
                            csv_dict[keys[index_line]] = [value.strip()]
                        else:
                            csv_dict[keys[index_line]].append(value.strip())
        return csv_dict
