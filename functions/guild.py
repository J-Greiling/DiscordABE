'''Base Functionality for guild managment'''

__author__ = "Jake Grey"
__date__ = "2021-03"

import discord
import csv
from . import guild_addon


class Guild:
    def __init__(self):
        filename = "./text/guild_save.csv"
        file_data = list(csv.reader(open(filename, "r"), delimiter=";"))
        self.bedroom_level = file_data[0][0]
        self.docks_level = file_data[0][1]
        self.kitchen_level = file_data[0][2]
        self.laboratory_level = file_data[0][3]
        self.pen_level = file_data[0][4]
        self.prison_level = file_data[0][5]
        self.scriptorium_level = file_data[0][6]
        self.smithy_level = file_data[0][7]
        self.stable_level = file_data[0][8]

        self.addons = {"bedroom": guild_addon.Addon(self.bedroom_level, "bedroom"),
                       "docks": guild_addon.Addon(self.docks_level, "docks"),
                       "kitchen": guild_addon.Addon(self.kitchen_level, "kitchen"),
                       "laboratory": guild_addon.Addon(self.laboratory_level, "laboratory"),
                       "pen": guild_addon.Addon(self.pen_level, "pen"),
                       "prison": guild_addon.Addon(self.prison_level, "prison"),
                       "scriptorium": guild_addon.Addon(self.scriptorium_level, "scriptorium"),
                       "smithy": guild_addon.Addon(self.smithy_level, "smithy"),
                       "stable": guild_addon.Addon(self.stable_level, "stable")}

    def get_embed(self):
        filename = "./text/guild.csv"
        guild_data = list(csv.reader(open(filename, "r"), delimiter=";"))
        embed = discord.Embed(
            title=guild_data[0][0],
            description=guild_data[0][1]
        )
        embed.set_thumbnail(url=guild_data[0][2])
        for value in self.addons.values():
            if(value.level):
                embed.add_field(name=value.title,
                                value=value.description,
                                inline=False)
        return embed






