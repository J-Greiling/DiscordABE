'''Resource Management for DiscordABE'''

__author__ = "Jakob Greiling"
__date__ = "2021-03"

import discord
from discord.ext import commands
from . import resource


class ResManagement(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.resource = resource.Resource()
        self.res_msg = 0

    @commands.command(name="storage", help="Information on Money and Ressource Managment of the Guild")
    async def print_storage(self, ctx):
        embed = discord.Embed(title="Storage")
        for i in range(len(self.resource.name)):
            if self.resource.max[i] == "0":
                embed.add_field(
                    name=f"{self.resource.name[i]}-{self.resource.emote[i]}",
                    value=f"{self.resource.current[i]}")
            else:
                embed.add_field(
                    name=f"{self.resource.name[i]}-{self.resource.emote[i]}",
                    value=f"{self.resource.current[i]} / {self.resource.max[i]}")

        msg = await ctx.send(embed=embed)
        self.res_msg = msg
        for emote in self.resource.emote:
            await msg.add_reaction(emote)

    @commands.command(name="add_money", help="Adds Money to the Guild")
    async def change_money(self, ctx, amount):
        await self.change_res(self, ctx, amount, "gold")

    @commands.command(name="add_res", help="Add Ressource to the guild (Syntax add <amount> <resource>)")
    async def change_res(self, ctx, amount, res):
        pass


def setup(bot):
    bot.add_cog(ResManagement(bot))

