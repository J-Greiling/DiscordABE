""" Main File for DiscordABE  """

__author__ = "Jake Grey"
__date__ = "2021-03"

# import
import os
import discord
from functions import *
from discord.ext import commands
from dotenv import load_dotenv

# load token

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

# setup bot
bot = commands.Bot(command_prefix="+")


@bot.event
async def on_ready():
    guild = discord.utils.get(bot.guilds)
    print("Discord Bot successfully started \nConnected Servers: \n"
          f"-{guild.name}")


@bot.command(name="template", help="Stat role syntax for Roll20")
async def template(ctx):
    template_embed = template_roll20.gen_embed()
    await ctx.send(embed=template_embed)


@bot.command(name="guild", help="general guild overview")
async def guildfun(ctx):
    guild_entity = guild.Guild()
    guild_embed = guild_entity.get_embed()
    await ctx.send(embed=guild_embed)
    await ctx.send(embed=guild_embed)

bot.run(TOKEN)
