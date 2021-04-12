'''Base Functionality for guild managment'''

__author__ = "Jake Grey"
__date__ = "2021-03"

import discord
import csv
import pandas as pd


class GuildData():
    def __init__(self):
        filename = "./text/addons.csv"
        self.addons = pd.read_csv(
            filename, delimiter=";", header=0, encoding="utf-8")
        self.addons["emoji"] = [emote.encode().decode("unicode-escape")
                                for emote in self.addons["emoji"]]

    def get_embed(self):
        """Embed fot the Guild listing all current upgrades"""
        filename = "./text/guild.csv"
        guild_data = list(csv.reader(open(filename, "r"), delimiter=";"))
        embed = discord.Embed(
            title=guild_data[0][0],
            description=guild_data[0][1]
        )
        embed.set_thumbnail(url=guild_data[0][2])

        # TODO DO NOT ITERRATE DF
        for i in range(len(self.addons)):
            if self.addons["current_level"][i] > 0:
                shift = self.addons["current_level"][i]
                idx_name = self.addons.columns.get_loc("name_level_0")
                idx_description = self.addons.columns.get_loc(
                    "description_level_0")
                embed.add_field(name=self.addons[self.addons.columns[idx_name + shift]][i],
                                value=self.addons[self.addons.columns[idx_description + shift]][i], inline=False)
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













