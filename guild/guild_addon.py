'''Addons for Guild '''

__author__ = "Jake Grey"
__date__ = "2021-03"

import csv


class Addon():
    def __init__(self, level: int, name: str):

        filename = f"./text/{name}.csv"
        file_text = list(csv.reader(open(filename, "r"), delimiter=";"))
        self.level = int(level)
        self.max_level = len(file_text) - 1
        self.title = file_text[self.level][0]
        self.description = file_text[self.level][1]




