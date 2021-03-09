""" Main File for DiscordABE  """

__author__ = "Jake Grey"
__date__ = "2021-03"

# import
import os
import discord
import random
import numpy as np
from discord.ext import commands
from dotenv import load_dotenv

# load token

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

# setup bot
bot = commands.Bot(command_prefix="+")

def add_markdown(msg_base: str):

    msg = f"```{msg_base}```"
    return msg


def roll_dice():
    dice = np.ones(4, dtype=int)
    for i in range(len(dice)):
        dice[i] = random.randrange(1, 7)
    dice = np.sort(dice)
    value = np.sum(np.delete(dice, 0))
    return value


if __name__ == "__main__":

    @bot.event
    async def on_ready():
        guild = discord.utils.get(bot.guilds)
        print("Discord Bot successfully started \nConnected Servers: \n"
              f"-{guild.name}")

    @bot.command(name="template", help="Stat role syntax for Roll20")
    async def temmplate(ctx):

        dice = np.ones(7, dtype=int)
        for i in range(len(dice)):
            dice[i] = roll_dice()

        dice = np.sort(dice)

        template_msg = add_markdown("[[4d6k3]][[4d6k3]][[4d6k3]][[4d6k3]][[4d6k3]][[4d6k3]]"
                                    f"\n\n Dice Rolls (it might be cursed): \n{dice} Sum: {np.sum(np.delete(dice,0))}")
        await ctx.send(template_msg)

    bot.run(TOKEN)
