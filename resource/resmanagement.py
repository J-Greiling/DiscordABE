'''Resource Management for DiscordABE'''

__author__ = "Jakob Greiling"
__date__ = "2021-03"

import discord
import pandas as pd
from discord.ext import commands

USER_ROLE = "Tyria"
DM_ROLE = "Regular DM"


class ResManagement(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        filename = "./text/resource.csv"
        self.resource = pd.read_csv(
            filename, delimiter=";", header=0, index_col=0, encoding="utf-8")
        self.resource["emoji"] = [emote.encode().
                                  decode("unicode-escape")
                                  for emote in self.resource["emoji"]]
        self.res_msg = 0

    @commands.command(name="storage", help="Information on Money and Ressource Managment of the Guild")
    async def print_storage(self, ctx):
        if any(USER_ROLE in role.name for role in ctx.message.author.roles):
            embed = discord.Embed(title="Storage")
            for resource in self.resource.index:
                if self.resource['max'][resource] == 0:
                    embed.add_field(
                        name=f"{self.resource['resource_name'][resource]}-{self.resource['emoji'][resource]}",
                        value=f"{self.resource['current'][resource]}")
                else:
                    embed.add_field(
                        name=f"{self.resource['resource_name'][resource]}-{self.resource['emoji'][resource]}",
                        value=f"{self.resource['current'][resource]} / {self.resource['max'][resource]}")

            msg = await ctx.send(embed=embed)
            self.res_msg = msg
            for emote in self.resource['emoji']:
                await msg.add_reaction(emote)

    @commands.command(name="add_money", help="Adds Money to the Guild")
    async def change_money(self, ctx, amount):
        if any(USER_ROLE in role.name for role in ctx.message.author.roles):
            await self.change_res(self, ctx, amount, "gold")

    @commands.command(name="add_res", help="Add Ressource to the guild (Syntax add <amount> <resource>)")
    async def change_res(self, ctx, amount, res):
        if any(USER_ROLE in role.name for role in ctx.message.author.roles):
            pass


def setup(bot):
    bot.add_cog(ResManagement(bot))


