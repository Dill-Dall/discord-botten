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
    for set in diceSets:
        set = set.split("d")
        set = [ str(random.choice(range(1, int(set[1])+ 1))) for _ in range(int(set[0])) ]
        sumOfDice = sum([int(i) for i in set])
        totalsum += sumOfDice
        diceValues = ','.join(set)
        diceStrings.append(f'{diceValues}={sumOfDice}')

    responseString=''
    for s in diceStrings:
        responseString += f'{s} : '

    await ctx.send(f">>> {responseString} = {totalsum}")

players = {}
