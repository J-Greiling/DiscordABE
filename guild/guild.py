'''Cog for Guild Managment'''

__author__ = "Jake Grey"
__date__ = "2021-03"

import discord
from discord.ext import commands
from . import guild_base


class Guild(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.guild = guild_base.GuildData()
        self.message = 0
        self.addon_message = 0
        self.confirmation_message = 0
        self.current_addon = ""

    @commands.command(name="guild", help="Gives overview for guild")
    async def print_guild(self, ctx):
        """Prints embed for Guild"""
        guild_embed = self.guild.get_embed()
        msg = await ctx.send(embed=guild_embed)
        self.message = msg
        await msg.add_reaction("\N{MONEY BAG}")
        for addon in self.guild.addon_names:
            if self.guild.addons[addon].level:
                await msg.add_reaction(self.guild.addon_emotes[self.guild.addon_names.index(addon)])
        await msg.add_reaction("\N{UPWARDS BLACK ARROW}")

    @commands.command(name="addon", help="Gives information about addon")
    async def print_addon(self, ctx, addon_name):
        """Prints embed for Addon"""
        if addon_name in self.guild.addon_names:
            embed = self.guild.get_addon_embed(addon_name)
            msg = await ctx.send(embed=embed)
            self.addon_message = msg
            if self.guild.addons[addon_name].level < self.guild.addons[addon_name].max_level:
                await msg.add_reaction("\N{UPWARDS BLACK ARROW}")
                self.current_addon = addon_name
        else:
            return

    @commands.command(name="addonlist", help="Prints list of all available addons")
    async def print_addonlist(self, ctx):
        """Prints embed of all addons"""
        embed = discord.Embed(
            title="List of Addons"
        )
        for addon in self.guild.addon_names:
            embed.add_field(
                name=self.guild.addons[addon].title,
                value=self.guild.addon_emotes[self.guild.addon_names.index(addon)], inline=False)
        message = await ctx.send(embed=embed)
        self.message = message
        for emote in self.guild.addon_emotes:
            await message.add_reaction(emote)

    @commands.command(name="upgrade", help="Upgrade an addon by one level")
    async def upgrade_addon(self, ctx, addon_name):
        if addon_name in self.guild.addon_names:
            if self.guild.addons[addon_name].level < self.guild.addons[addon_name].max_level:
                self.guild.upgrade_addon(addon_name)

    @commands.Cog.listener()
    async def on_reaction_add(self, react, react_user):
        channel = react.message.guild.system_channel

        if self.message:
            if react.message.id == self.message.id:
                if react.count > 1 and react.emoji in self.guild.addon_emotes:
                    self.current_addon = self.guild.addon_names[self.guild.addon_emotes.index(
                        react.emoji)]
                    await self.print_addon(channel, self.current_addon)
                if react.count > 1 and react.emoji == "\N{UPWARDS BLACK ARROW}":
                    await self.print_addonlist(channel)
                if react.count > 1 and react.emoji == "\N{MONEY BAG}":
                    res_mangament = self.bot.get_cog(
                        "ResManagement")
                    await res_mangament.print_storage(channel)

        if self.addon_message:
            if react.message.id == self.addon_message.id:
                if react.emoji == "\N{UPWARDS BLACK ARROW}" and react.count > 1:
                    msg = await channel.send("Do you really want to Upgrade?")
                    self.confirmation_message = msg
                    await msg.add_reaction("\N{WHITE HEAVY CHECK MARK}")

        if self.confirmation_message:
            if react.message.id == self.confirmation_message.id:
                if react.emoji == "\N{WHITE HEAVY CHECK MARK}" and react.count == 2:
                    self.guild.upgrade_addon(self.current_addon)
                    await self.print_addon(channel, self.current_addon)


def setup(bot):
    bot.add_cog(Guild(bot))














