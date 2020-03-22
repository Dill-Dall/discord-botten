# bot.py
import os
import random 

import discord
from discord.ext import commands
from dotenv import load_dotenv

import quotelist

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

bot = commands.Bot(command_prefix='!')

@bot.command(name='99', help='Responds with a random quote from Brooklyn 99')
async def nine_nine(ctx):
    brooklyn_99_quotes = [
        'I\'m the human form of the 💯 emoji.',
        'Bingpot!',
        '99!',
        "“Sarge, with all due respect, I am gonna completely ignore everything you just said.” – Jake Peralta",
        "“A place where everybody knows your name is hell. You’re describing hell.” – Rosa Diaz",
        "“If I die, turn my tweets into a book.” – Gina Linetti",
        "“Great, I’d like your $8-est bottle of wine, please.” – Jake Peralta",
        "“Captain Wuntch. Good to see you. But if you’re here, who’s guarding Hades?” – Captain Holt",
        "“Anyone over the age of six celebrating a birthday should go to hell.” – Rosa Diaz",
        "“Jake, piece of advice: just give up. It’s the Boyle way. It’s why our family crest is a white flag.” – Charles Boyle",
        (
            'Cool. Cool cool cool cool cool cool cool, '
            'no doubt no doubt no doubt no doubt.'
        ),
    ]

    response = random.choice(brooklyn_99_quotes)
    await ctx.send(response)

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

@bot.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f'Hi {member.name}, welcome to {GUILD}!'
    )


def check(author):
    def inner_check(message):
        return message.author == author
    return inner_check

def testContent(message, answer):
    answerList = answer.lower().split(",")
    if message.lower() in answerList: return True
    return False


@bot.command(name='quiz', help='Starts a quiz about game quotes.')
async def quiz_me(ctx):

    quoteObject = random.choice(quotelist.quoteObjectList)
    await ctx.send(f'{ctx.author} The quote: {quoteObject.quote}')
    if(quoteObject.npc != ""):
        await ctx.send("Was said by?")
        reply = await bot.wait_for('message', check=check(ctx.author), timeout=30)
        if(testContent(reply.content, quoteObject.npc)): await ctx.send(reply.content+" is correctomundo")
        else: await ctx.send(reply.content+" is fail")

    await ctx.send("Was said in which game?")
    reply = await bot.wait_for('message', check=check(ctx.author), timeout=30)
    if(testContent(reply.content, quoteObject.game)): await ctx.send(reply.content+" is correctomundo")
    else: await ctx.send(reply.content+" is fail")



@bot.command(name='roll', help='!roll 3d4 could give 3,1,2 = 6')
async def roll(ctx, diceString):

    dice = diceString.split("d")


    dice = [
        str(random.choice(range(1, int(dice[1])+ 1)))
        for _ in range(int(dice[0]))
    ]

    sumOfDice = sum([int(i) for i in dice])
    diceValues  = ', '.join(dice)

    await ctx.send(f"{diceValues}={sumOfDice}")




bot.run(TOKEN)