"""
    Module to handle rolling of dice
"""
import string
import random

from discord.ext import commands

class Diceroller(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(help='!roll 3d4 could give 3,1,2 = 6.. !roll 2d20 +3d10, could give "18,17=35 : 8,1,6=15 :  = 50"')
    async def roll(self, ctx, *args):
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

    # players = {} # why is this here?
