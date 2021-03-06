"""Cog for Guild Management"""

__author__ = "Jakob Greiling"
__date__ = "2021-04"

# imports
import discord
from discord.ext import commands
from . import guild_base

# globals
USER_ROLE = "Tyria"
DM_ROLE = "Regular DM"
BOT_ROLE = "A.B.E"


class Guild(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.guild = guild_base.GuildData()
        self.res_management = bot.get_cog("ResManagement")
        self.message = None
        self.addon_message = None
        self.confirmation_message = None
        self.current_addon = None

    @commands.command(name="guild", help="Gives overview for guild")
    @commands.has_any_role(USER_ROLE, BOT_ROLE)
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
    @commands.has_any_role(USER_ROLE, BOT_ROLE)
    async def print_addon(self, ctx, addon_name: str):
        """Prints embed for Addon

        Parameters
        ----------
        addon_name - Name of addon to be unlocked
        """
        try:
            addon_name = addon_name.lower()
            if self.guild.addon_unlocked(addon_name):
                addon_level = self.guild.addons["current_level"][addon_name]
                addon_max_level = self.guild.addons["max_level"][addon_name]
                embed = self.guild.get_addon_embed(addon_name, addon_level, addon_max_level)
                msg = await ctx.send(embed=embed)
                self.addon_message = msg
                if addon_level < addon_max_level:
                    await msg.add_reaction("\N{UPWARDS BLACK ARROW}")
                    self.current_addon = addon_name

            else:
                await ctx.send("Stop Meta gaming")

        except Exception as e:
            print(f"Invalid input in {self.print_addon.name}: {e}")
            await ctx.send("Invalid Addon name")

    @commands.command(name="addonlist", help="Prints list of all available addons")
    @commands.has_any_role(USER_ROLE, BOT_ROLE)
    async def print_addonlist(self, ctx):
        """Prints embed of all addons"""
        embed = discord.Embed(
            title="List of Addons"
        )

        for addon in self.guild.addons.index:
            if self.guild.addon_unlocked(addon):
                level = self.guild.addons["current_level"][addon]
                embed.add_field(
                    name=f"{self.guild.addons[self.guild.get_shift_name(level)][addon]}"
                         f" - {self.guild.addons['emoji'][addon]}",
                    value=self.guild.addons[self.guild.get_shift_description(level)][addon],
                    inline=False)

        msg = await ctx.send(embed=embed)
        self.message = msg

        for addon in self.guild.addons.index:
            if self.guild.addon_unlocked(addon):
                await msg.add_reaction(self.guild.addons['emoji'][addon])

    @commands.command(name="upgrade", help="Upgrade an addon by one level")
    @commands.has_any_role(USER_ROLE, BOT_ROLE)
    async def upgrade_addon(self, ctx, addon_name: str):
        """Upgrade addon to next level

        Parameters
        ---------
        addon_name - Name of addon to be upgraded
        """
        try:
            addon_name = addon_name.lower()
            addon_level = self.guild.addons["current_level"][addon_name]
            addon_max_level = self.guild.addons["max_level"][addon_level]
            if addon_level < addon_max_level:
                addon = self.guild.addons[self.guild.get_shift_name(addon_level + 1)][addon_name]

                missing_res = self.guild.costs[self.guild.costs[addon] >
                                               self.res_management.resource["current"]].index

                if len(missing_res) > 0:
                    for res in missing_res:
                        missing_value = self.guild.costs[addon][res] - \
                                        self.res_management.resource["current"][res]
                        await ctx.send(f"Missing {missing_value} {res}")
                        # TODO Buy Missing res

                else:
                    for res in self.guild.costs.index:
                        await self.res_management.add_res(ctx, -self.guild.costs[addon][res], res)

                    self.guild.addons.at[addon_name, "current_level"] = addon_level + 1
                    self.guild.save_addons()
                    await self.print_addon(ctx, addon_name)

            else:
                await ctx.print("Maximum level of Addon reached")

        except Exception as e:
            print(f"Invalid input in {self.upgrade_addon.name}: {e}")
            await ctx.send("Invalid Addon name")

    @commands.command(name="unlock", help="Function to unlock new addons (DM-only)")
    @commands.has_any_role(DM_ROLE, BOT_ROLE)
    async def unlock_addon(self, ctx, addon_name: str):
        """Unlocks unavailable addons for the players to purchase

        Parameters
        ----------
        addon_name - Name of Addon to be unlocked
        """

        try:
            if addon_name in self.guild.addons.index:
                addon_name = addon_name.lower()
                self.guild.addons.at[addon_name, "unlocked"] = 1
                self.guild.save_addons()
                await ctx.message.add_reaction("\N{WHITE HEAVY CHECK MARK}")

        except Exception as e:
            print(f"Invalid input in {self.unlock_addon.name}: {e}")
            await ctx.send("Invalid Addon name")

    @commands.command(name="update", help="Pass a month, processing guild activities (DM-Only)")
    @commands.has_any_role(DM_ROLE, BOT_ROLE)
    async def update_guild(self, ctx):
        """Passes a month deducting money and processing goods
        For now just money deduction is implemented
        """
        upkeep = 0
        for addon in self.guild.addons.index:
            upkeep += self.guild.addons["current_level"][addon] * 20
        await ctx.send(f"Current Upkeep: {upkeep} Gold")
        await self.res_management.add_money(ctx, -upkeep)


    @commands.Cog.listener()
    async def on_reaction_add(self, react, react_user):
        """Listener Function to handle Reactions"""

        if any(USER_ROLE in role.name for role in react_user.roles):
            # TODO FIX "unintended Reaction" from Users without Tyria Role,
            # low priority as people able to invoke this message are likely to do it in the respective channel
            ctx = await self.bot.get_context(react.message)

            if self.message:
                if react.message.id == self.message.id:
                    for addon in self.guild.addons.index:
                        if react.count > 1 and react.emoji == self.guild.addons["emoji"][addon]:
                            await self.print_addon(ctx, addon)

                    if react.count > 1 and react.emoji == "\N{UPWARDS BLACK ARROW}":
                        await self.print_addonlist(ctx)

                    if react.count > 1 and react.emoji == "\N{MONEY BAG}":
                        await self.res_management.print_storage(ctx)

            if self.addon_message:
                if react.message.id == self.addon_message.id:
                    if react.emoji == "\N{UPWARDS BLACK ARROW}" and react.count > 1:
                        msg = await ctx.send("Do you really want to Upgrade?")
                        self.confirmation_message = msg
                        await msg.add_reaction("\N{WHITE HEAVY CHECK MARK}")
                        await msg.add_reaction("\N{CROSS MARK}")

            if self.confirmation_message:
                if react.message.id == self.confirmation_message.id:
                    if react.emoji == "\N{WHITE HEAVY CHECK MARK}" and react.count > 1:
                        await self.upgrade_addon(ctx, self.current_addon)

                    if react.emoji == "\N{CROSS MARK}" and react.count > 1:
                        self.confirmation_message = None


def setup(bot):
    """"Setup for Bot COG Initialization"""
    bot.add_cog(Guild(bot))
