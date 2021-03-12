'''Base Functionality for guild managment'''

__author__ = "Jake Grey"
__date__ = "2021-03"

import discord
import os


def read_file(filename: str):
    os.chdir("./text/")
    file = open(filename, "r")
    return file.read()


def get_embed():
    title_desc_text = read_file("guild_description.txt")
    embed = discord.Embed(
        title="Guild of Rata Sum",
        description=title_desc_text
    )
    return embed


