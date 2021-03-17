'''Cog for Guild Managment'''

__author__ = "Jake Grey"
__date__ = "2021-03"

import discord
from discord.ext import commands
from . import guild_addon
from . import guild_base


class Guild(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.guild = guild_base.GuildData()

    @commands.command(name="guild", help="Gives overview for guild")
    async def print_guild(self, ctx):
        """Prints embed for Guild"""
        guild_embed = self.guild.get_embed()
        await ctx.send(embed=guild_embed)

    @commands.command(name="addon", help="Gives information about addon")
    async def print_addon(self, ctx, addon_name):
        """Prints embed for Addon"""
        if addon_name in self.guild.addon_names:
            addon_data = self.guild.addons[addon_name]
            current_upgrade = guild_addon.Addon(
                addon_data.level + 1, addon_name)
            embed = discord.Embed(
                title=addon_data.title,
                description=addon_data.description
            )
            embed.add_field(
                name="Next Upgrade",
                value=current_upgrade.description
            )
            await ctx.send(embed=embed)
        else:
            pass

    @commands.command(name="addonlist", help="Prints list of all available addons")
    async def print_addonlist(self, ctx):
        embed = discord.Embed(
            title="List of Addons"
        )
        i = 0
        for value in self.guild.addons.values():
            embed.add_field(name=value.title,
                            value=self.guild.addon_emotes[i],
                            inline=False)
            i += 1

        message = await ctx.send(embed=embed)
        for emote in self.guild.addon_emotes:
            await message.add_reaction(emote)


def setup(bot):
    bot.add_cog(Guild(bot))














