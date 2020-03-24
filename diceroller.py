import string
import random

async def roll(ctx, *args):
    diceString = ''.join(args)
    dice = diceString.translate({ord(c): None for c in string.whitespace})

    #[2d4,4d8]
    diceSets = dice.split("+")
    diceStrings = []
    totalsum = 0
    #[[2,4],[4,8]]
    for dice_set in diceSets:
        dice_set = dice_set.split("d")
        dice_set = [str(random.choice(range(1, int(dice_set[1])+ 1))) for _ in range(int(dice_set[0]))]
        sumOfDice = sum([int(i) for i in dice_set])
        totalsum += sumOfDice
        diceValues = ','.join(dice_set)
        diceStrings.append(f'{diceValues}={sumOfDice}')

    responseString=''
    for s in diceStrings:
        responseString += f'{s} : '

    await ctx.send(f">>> {responseString} = {totalsum}")

players = {}
