'''Cog for Guild Managment'''

__author__ = "Jake Grey"
__date__ = "2021-03"

import discord
import string
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

        for addon in self.guild.addons.index:
            if self.guild.addons["current_level"][addon]:
                await msg.add_reaction(self.guild.addons["emoji"][addon])
        await msg.add_reaction("\N{UPWARDS BLACK ARROW}")

    @commands.command(name="addon", help="Gives information about addon")
    async def print_addon(self, ctx, addon_name):
        """Prints embed for Addon"""
        addon_name = addon_name.lower()

        try:
            if(self.guild.addon_unlocked(addon_name)):
                addon_level = self.guild.addons["current_level"][addon_name]
                addon_max_level = self.guild.addons["max_level"][addon_name]
                embed = self.guild.get_addon_embed(
                    addon_name, addon_level, addon_max_level)
                msg = await ctx.send(embed=embed)
                self.addon_message = msg
                if addon_level < addon_max_level:
                    await msg.add_reaction("\N{UPWARDS BLACK ARROW}")
                    self.current_addon = addon_name
            else:
                await ctx.send("Stop Metagaming")
        except:
            await ctx.send("Invalid Addon name")

    @commands.command(name="addonlist", help="Prints list of all available addons")
    async def print_addonlist(self, ctx):
        """Prints embed of all addons"""
        embed = discord.Embed(
            title="List of Addons"
        )

        for addon in self.guild.addons.index:
            if self.guild.addon_unlocked(addon):
                level = self.guild.addons["current_level"][addon]
                embed.add_field(
                    name=f"{self.guild.addons[self.guild.get_shift_name(level)][addon]} - {self.guild.addons['emoji'][addon]}", value=self.guild.addons[self.guild.get_shift_description(level)][addon], inline=False)

        msg = await ctx.send(embed=embed)
        self.message = msg

        for addon in self.guild.addons.index:
            if self.guild.addon_unlocked(addon):
                await msg.add_reaction(self.guild.addons['emoji'][addon])

    @commands.command(name="upgrade", help="Upgrade an addon by one level")
    async def upgrade_addon(self, ctx, addon_name):
        # try:
        addon_name = addon_name.lower()
        addon_level = self.guild.addons["current_level"][addon_name]
        addon_max_level = self.guild.addons["max_level"][addon_level]
        # TODO Check for cost
        if addon_level < addon_max_level:
            self.guild.upgrade_addon(addon_name, addon_level)

        # except:
        #    await ctx.send("Invalid Addon name")

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














