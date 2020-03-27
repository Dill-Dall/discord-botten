"""
    Module to handle rolling of dice
"""
import random

from discord.ext import commands

class Diceroller(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # TODO Update help text
    # Possibly make it a dosctring instead
    @commands.command(help='!roll 3d4 could give 3,1,2 = 6.. !roll 2d20 3d10, could give "18,17=35 : 8,1,6=15 :  = 50"')
    async def roll(self, ctx, *args):
        dice = args
        total_sum = 0
        full_response = []

        for die in dice:
            number_of_die = int(die.split("d")[0])
            die_value = int(die.split("d")[1])
            dice_values = [str(random.randint(1, die_value)) for i in range(number_of_die)]
            sum_of_dice = sum(int(i) for i in dice_values) 
            total_sum += sum_of_dice

            if number_of_die == 1:
                response = f"{die} : {sum_of_dice}"
            else:
                response = f"{die}: {'+'.join(dice_values)} = {sum_of_dice}"
            full_response.append(response)

        if len(full_response) > 1:
            # Can't have backslash inside expression in an f-string.
            # "chr(10)" gets the character that represents unicode 10, which is "\n"
            await ctx.send(f">>> {chr(10).join(full_response)}\nTotal sum = {total_sum}")
        else:
            await ctx.send(f">>> {''.join(full_response)}")
