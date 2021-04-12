'''Base Functionality for guild managment'''

__author__ = "Jake Grey"
__date__ = "2021-03"

import discord
import csv
from . import guild_addon


class GuildData():
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
        self.addon_names = ["bedroom", "docks", "kitchen", "laboratory",
                            "pen", "prison", "scriptorium", "smithy", "stable"]
        self.addon_emotes = ["\N{BED}", "\N{SAILBOAT}", "\N{FORK AND KNIFE}", "\N{ALEMBIC}",
                             "\N{CHICKEN}", "\N{LOCK}", "\N{SCROLL}", "\N{HAMMER}", "\N{HORSE}"]

    def get_embed(self):
        """Embed fot the Guild listing all current upgrades"""
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

    def get_addon_embed(self, addon_name):
        """Embed of one addon showing the next upgrade if possible"""
        addon_data = self.addons[addon_name]

        embed = discord.Embed(
            title=addon_data.title,
            description=addon_data.description
        )

        if self.addons[addon_name].level < self.addons[addon_name].max_level:
            current_upgrade = guild_addon.Addon(
                addon_data.level + 1, addon_name)
            embed.add_field(
                name="Next Upgrade",
                value=current_upgrade.description
            )
        return embed

    def upgrade_addon(self, addon_name):
        """Upgrade the addon by one level and saves levels"""

        # Checks for valitiy are done before function call
        self.addons[addon_name] = guild_addon.Addon(
            self.addons[addon_name].level + 1, addon_name)

        # save current level
        filename = "./text/guild_save.csv"
        writer = csv.writer(open(filename, "w"), delimiter=";")
        writer.writerow(
            [self.addons[addon].level for addon in self.addon_names])













