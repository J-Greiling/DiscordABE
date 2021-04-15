""" Main File for DiscordABE  """

__author__ = "Jake Grey"
__date__ = "2021-03"

# import
import os
import discord

from discord.ext import commands
from dotenv import load_dotenv

# load token

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

# setup bot
bot = commands.Bot(command_prefix="+")

# load COGS
bot.load_extension("custom.custom_commands")
bot.load_extension("resource.resmanagement")
bot.load_extension("guild.guild")

# startup


@bot.event
async def on_ready():
    guild = discord.utils.get(bot.guilds)
    print("Discord Bot successfully started \nConnected Servers: \n"
          f"-{guild.name}")


bot.run(TOKEN)
