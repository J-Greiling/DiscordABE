'''Base Functionality for guild managment'''

__author__ = "Jake Grey"
__date__ = "2021-03"

import discord
import os
import csv


def read_file(filename: str):
    return list(csv.reader(open(filename, "r"), delimiter=";"))


def get_embed():
    title_desc_text = read_file("guild_description.csv")
    embed = discord.Embed(
        title="Guild of Rata Sum",
        description=title_desc_text
    )
    return embed


if __name__ == "__main__":
    os.chdir("../text/")
    filename = "smithy.csv"

    file_csv = list(csv.reader(open(filename, "r"), delimiter=";"))
    print(file_csv[0][0])




