""" Main File for DiscordABE  """

__author__ = "Jake Grey"
__date__ = "2021-03"

# import
import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

# load token
TOKEN = os.getenv("DISCORD_TOKEN")

# setup bot

bot = commands.Bot(command_prefix="+")


if __name__ == "__main__":

    @bot.event
    async def on_ready():
        guild = discord.utils.get(bot.guilds)
        print("Discord Bot successfully started \n "
              f"-{guild.name}")

    @bot.command(name="template", help="Stat role syntax for Roll20")
    async def temmplate(ctx):

        template_msg = "[4d6k3][4d6k3][4d6k3][4d6k3][4d6k3][4d6k3]"
        await ctx.send(template_msg)


bot.run(TOKEN)
