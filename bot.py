""" Main File for DiscordABE  """

__author__ = "Jake Grey"
__date__ = "2021-04"

# import
import os
import discord

from discord.ext import commands
from dotenv import load_dotenv

# load token
load_dotenv()
TOKEN = os.getenv("TEST_TOKEN")

# setup bot
bot = commands.Bot(command_prefix="-")


# load COGS
bot.load_extension("custom.custom_commands")
bot.load_extension("resource.resmanagement")
bot.load_extension("guild.guild")


# startup
@bot.event
async def on_ready():
    guild = bot.guilds
    print("Discord Bot successfully started \n"
          f"Connected as {bot.user}\n"
          "Connected Servers: \n")
    for guild_entry in guild:
        print(f"-{guild_entry.name}")


bot.run(TOKEN)
