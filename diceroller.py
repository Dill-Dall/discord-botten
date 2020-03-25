"""
    Module to handle rolling of dice
"""
import string
import random

async def roll(ctx, *args):
    dice_strings = ''.join(args)
    dice = dice_strings.translate({ord(c): None for c in string.whitespace})

    #[2d4,4d8]
    dice_sets = dice.split("+")
    dice_strings = []
    totalsum = 0
    #[[2,4],[4,8]]
    for dice_set in dice_sets:
        dice_set = dice_set.split("d")
        dice_set = [str(random.choice(range(1, int(dice_set[1])+ 1))) for _ in range(int(dice_set[0]))]
        sum_of_dice = sum([int(i) for i in dice_set])
        totalsum += sum_of_dice
        dice_values = ','.join(dice_set)
        dice_strings.append(f'{dice_values}={sum_of_dice}')

    response_string = ''
    for dice_string in dice_strings:
        response_string += f'{dice_string} : '

    await ctx.send(f">>> {response_string} = {totalsum}")

players = {} # why is this here?
