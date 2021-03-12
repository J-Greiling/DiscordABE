'''Dice rolls managment'''

__author__ = "Jake Grey"
__date__ = "2021-03"

import random
import numpy as np


def roll_dice(n: int, x: int):
    '''Rolls n, x sided dice

    Params:
    -------
       n - amount of dice
       x - amount of sides

    Returns:
    -------
       roll - array of rolled dice
    '''

    roll = np.ones(n, dtype=int)
    for i in range(n):
        roll[i] = random.randrange(1, x + 1)

    return roll


def roll_keep(n: int, x: int, y: int):
    ''' Rolls multiple dice and keeps a defined amount

    Params:
    -------
       n - amount of dice
       x - sides of the dice
       k - amount to keep

    Returns:
    --------
       roll_selection - array of dice after selection
    '''

    roll = roll_dice(n, x)
    roll_selection = np.delete(np.sort(roll), range(n - y))

    return roll_selection


