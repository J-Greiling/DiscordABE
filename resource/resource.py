'''Money Managment'''

__author__ = "Jakob Greiling"
__date__ = "2021-03"

import csv


class Resource():
    def __init__(self):
        filename = "./text/resource.csv"
        file_data = list(csv.reader(open(filename, "r"), delimiter=";"))
        self.name = file_data[0]
        self.emote = [data.encode().decode("unicode-escape")
                      for data in file_data[1]]
        self.max = file_data[2]
        self.current = file_data[3]


