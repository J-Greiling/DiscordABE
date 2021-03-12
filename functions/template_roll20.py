'''Function for roll20 dice roll template generation'''

__author__ = "Jake Grey"
__date__ = "2021-03"

import numpy as np
import discord
from . import dice


def gen_embed():
    '''Function to generate the embed for the discord message'''

    dice_rolls = np.ones(7, dtype=int)
    for i in range(len(dice_rolls)):
        dice_rolls[i] = np.sum(dice.roll_keep(4, 6, 3))

    dice_sorted = np.sort(dice_rolls)

    embed = discord.Embed(
        title="Template for Roll 20",
        description="[[4d6k3]][[4d6k3]][[4d6k3]][[4d6k3]][[4d6k3]][[4d6k3]][[4d6k3]]"
    )
    embed.add_field(
        name="Rolls (might be cursed)",
        value=f"{dice_sorted}",
        inline=True
    )
    embed.add_field(
        name="Sum of dice (lowest dropped)",
        value=f"{np.sum(np.delete(dice_sorted,0))}",
        inline=True
    )
    embed.set_footer(text="No takebacks for bad rolls")

    return embed


if __name__ == "__main__":

    gen_embed()


