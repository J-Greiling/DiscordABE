"""Resource Management for DiscordABE"""

__author__ = "Jakob Greiling"
__date__ = "2021-04"

# import
import discord
import pandas as pd
from discord.ext import commands

# globals
USER_ROLE = "Tyria"
DM_ROLE = "Regular DM"
BOT_ROLE = "A.B.E"

class ResManagement(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        filename = "./text/resource.csv"
        self.resource = pd.read_csv(
            filename, delimiter=";", header=0, index_col=0, encoding="utf-8")
        self.res_msg = None

    @commands.command(name="storage", help="Information on Money and Resource Management of the Guild")
    @commands.has_any_role(USER_ROLE, BOT_ROLE)
    async def print_storage(self, ctx):
        """Function to print the storage of Guild"""
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

    @commands.command(name="buy_res", help="Buy Resource to the guild (Syntax add <amount> <resource>)")
    @commands.has_any_role(USER_ROLE, BOT_ROLE)
    async def buy_res(self, ctx, amount: str, res: str):
        """Function to buy Resources for predefined prices

        Parameters
        ----------
        amount - amount of res to be sold
        res - resource to be bought
        """
        try:
            amount = int(amount)
            value_new_res = self.resource["value"][res.lower()] * amount
            if value_new_res <= self.resource["current"]["gold"]:
                if amount > 0 or abs(amount) <= self.resource["current"][res.lower()]:
                    self.resource.at["gold", "current"] = self.resource["current"]["gold"] - value_new_res
                    await self.add_res(ctx, amount, res)
                else:
                    await ctx.send(f"Storage Insufficient to modify {res} by {abs(amount)}")
            else:
                value_missing = value_new_res - \
                                self.resource["current"]["gold"]
                await ctx.send(f"Insufficient funds to buy {res}, missing {value_missing} Gold")
        except BaseException as e:
            print(f"Invalid input in {self.buy_res.name}: {e}")
            await ctx.send("Invalid Input")

    @commands.command(name="sell_res", help="Sell Resource from the guild (Syntax sell <amount> <resource>)")
    @commands.has_any_role(USER_ROLE, BOT_ROLE)
    async def sell_res(self, ctx, amount: str, res: str):
        """Alias for Function buy res with a negative Value
        Converts positive Value to negative and calls self.buy_res

        Parameters
        ----------
        amount - amount of res to be sold
        res - resource to be sold, check for validity in buy_res
        """
        await self.buy_res(ctx, -amount, res)

    @commands.command(name="add_money", help="Adds Money to the Guild (DM only)")
    @commands.has_any_role(DM_ROLE, BOT_ROLE)
    async def add_money(self, ctx, amount: str):
        """"DM Function to add money to the Guild, no perquisites need to be met to add

        Parameters
        ----------
        amount - Amount of money to be added to the guild
        """
        try:
            await self.add_res(ctx, amount, "gold")
        except BaseException as e:
            print(f"Invalid input in {self.add_money.name}: {e}")
            await ctx.send("Invalid Input")

    @commands.command(name="add_res", help="Add Resource to the guild (DM only)")
    @commands.has_any_role(DM_ROLE, BOT_ROLE)
    async def add_res(self, ctx, amount: str, res: str):
        try:
            current_res = self.resource["current"][res.lower()]
            max_res = self.resource["max"][res.lower()]
            amount = int(amount)
            if max_res and current_res + amount > max_res:
                remainder_res = current_res + amount - max_res
                remainder_value = remainder_res * self.resource["value"][res.lower()]
                await ctx.send(
                    f"Maximum Capacity reached, selling/refunding {remainder_res} {res} for {remainder_value} Gold")
                self.resource.at[res.lower(), "current"] = max_res
                self.resource.at["gold",
                                 "current"] = self.resource["current"]["gold"] + remainder_value
            else:
                if amount > 0 or abs(amount) <= current_res:
                    self.resource.at[res.lower(
                    ), "current"] = current_res + amount
                else:
                    await ctx.send(f"Storage insufficient to modify {res} by {abs(amount)}")

            # confirm Input
            await ctx.message.add_reaction("\N{WHITE HEAVY CHECK MARK}")

            filename = "./text/resource.csv"
            self.resource.to_csv(path_or_buf=filename, sep=";")
        except BaseException as e:
            print(f"Invalid input in {self.add_res.name}: {e}")
            await ctx.send("Invalid Input")

    async def buy_res_direct(self, ctx, res: str, user):
        """Interactive Input based on reaction, asks user the amount of selected resource to be modified

        Parameters
        ----------
        res - resource to be added
        """
        await ctx.send(f"How much {res} do you want to buy? (negative number to sell)")

        def check(m):
            return m.author == user and m.channel == ctx.message.channel

        msg = await self.bot.wait_for('message', check=check)
        await self.buy_res(ctx, msg.content, res.lower())

    async def edit_res_upkeep(self, res: str):
        """Removes up to ten of a Resource to be converted to gold

        Paramters
        ---------
           res - Name of resource to be taken from storage

        Returns
        -------
           amount - amount of res for conversion
        """
        threshold = 10
        if res == "wood":
            threshold *= 2
        if self.resource["current"][res] > threshold:
            amount = threshold
            self.resource.at[res, "current"] = self.resource["current"][res] - threshold
        else:
            amount = self.resource["current"][res]
            self.resource.at[res, "current"] = 0
        return amount

    @commands.Cog.listener()
    async def on_reaction_add(self, react, react_user):
        """Listener Function to handle Reactions"""

        ctx = await self.bot.get_context(react.message)

        if self.res_msg:
            if react.message.id == self.res_msg.id:
                for res in self.resource.index:
                    if react.count > 1 and react.emoji == self.resource["emoji"][res]:
                        await self.buy_res_direct(ctx, res, react_user)


def setup(bot):
    """"Setup for Bot COG Initialization"""
    bot.add_cog(ResManagement(bot))
