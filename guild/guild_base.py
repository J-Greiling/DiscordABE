"""Base Functionality for guild management"""

__author__ = "Jakob Greiling"
__date__ = "2021-04"

# import
import discord
import csv
import pandas as pd


class GuildData:
    def __init__(self):
        filename = "./text/addons.csv"
        self.addons = pd.read_csv(
            filename, delimiter=";", header=0, index_col=0, encoding="utf-8")
        filename = "./text/cost.csv"
        self.costs = pd.read_csv(
            filename, delimiter=";", header=0, index_col=0, encoding="utf-8")

    def get_embed(self):
        """Embed fot the Guild listing all current upgrades

        Returns
        -------
            discord.Embed of guild information and current addons

        """
        filename = "./text/guild.csv"
        guild_data = list(csv.reader(open(filename, "r"), delimiter=";"))
        embed = discord.Embed(
            title=guild_data[0][0],
            description=guild_data[0][1])
        embed.set_thumbnail(url=guild_data[0][2])

        for addon in self.addons.index:
            if self.addons["current_level"][addon] > 0:
                level = self.addons["current_level"][addon]
                embed.add_field(
                    name=self.addons[self.get_shift_name(level)][addon],
                    value=self.addons[self.get_shift_description(level)][addon],
                    inline=False)
        return embed

    def get_shift_name(self, level):
        """Function to find header index shifted by level name_level_0

        Parameters
        ----------
        level - Current level of addon

        Returns
        -------
            Header value shifted to compensate for level > 0
        """

        idx_name = self.addons.columns.get_loc("name_level_0")
        return self.addons.columns[idx_name + level]

    def get_shift_description(self, level):
        """Function to find header shifted by level from description_level_0

        Parameters
        ----------
        level - Current level of addon

        Returns
        -------
        Header value shifted to compensate for level > 0
        """

        idx_description = self.addons.columns.get_loc("description_level_0")
        return self.addons.columns[idx_description + level]

    def addon_unlocked(self, addon_name):
        """Check if Addon is unlocked

        Parameters
        ----------
        addon_name - Name of addon to be checked

        Returns
        -------
        0/1 determined if by unlock stadium of addon
        """

        return self.addons["unlocked"][addon_name]

    def get_addon_embed(self, addon_name, level, max_level):
        """Embed of one addon showing the next upgrade if possible

        Parameters
        ----------
        addon_name - Name of Addon to be checked
        level - Current Level of addon
        max_level - Maximum level of current addon

        Returns
        -------
        discord.Embed of current addon status and description of next update

        """

        embed = discord.Embed(
            title=self.addons[self.get_shift_name(level)][addon_name],
            description=self.addons[self.get_shift_description(level)][addon_name])

        if level < max_level:
            embed.add_field(
                name="Next Upgrade",
                value=self.addons[self.get_shift_description(level + 1)][addon_name],
                inline=False)

            for res in self.costs.index:
                res_value = self.costs[self.addons[self.get_shift_name(
                    level + 1)][addon_name]][res]
                if res_value:
                    embed.add_field(name=res,
                                    value=res_value,
                                    inline=True)

        return embed

    def save_addons(self):
        """Saves addons dataframe"""
        filename = "./text/addons.csv"
        self.addons.to_csv(path_or_buf=filename, sep=";")
