# bot.py
import os
import random 
import enum
import discord
import string
import youtube_dl
import json

from discord.ext import commands
from dotenv import load_dotenv

import quotelist

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

bot = commands.Bot(command_prefix='!')

class StringStyle(enum.Enum):
   YELLOW= "fix"
   CYAN="yaml"
   DIFF="diff"
   NONE=""


def sWrap(string, stringStyle):
    return f""">>> ```{stringStyle.value}\n{string}```"""

@bot.command(name='99', help='Responds with a random quote from Brooklyn 99')
async def nine_nine(ctx):
    response = random.choice(quotelist.brooklyn_99_quotes)
    await ctx.send(response)

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

@bot.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f'>>> Hi {member.name}, welcome to {GUILD}!'
    )

@bot.command()
async def avatar(ctx, member: discord.Member):
    show_avatar = discord.Embed(
        color = discord.Color.dark_blue()
    )
    show_avatar.set_image(url='{}'.format(member.avatar_url))
    await ctx.send(embed=show_avatar)

def check(author):
    def inner_check(message):
        return message.author == author
    return inner_check

def testContent(message, answer):
    answerList = answer.lower().split(",")
    if message.lower() in answerList: return True
    return False


with open("quotequiz.json", "r") as file:
    QUOTELIST = json.load(file)

with open("score.json", "r") as file:
    SCORECARD = json.load(file)

def addPoint(name):
    with open("score.json", "w") as file:
        for p in SCORECARD:
            if(p["name"] == name):
                p["score"] = str(int(p["score"]) + 1)
                json.dump(SCORECARD, file, indent=4)
    
    

@bot.command(name='quiz', help='Starts a quiz about quotes.')
async def quiz_me(ctx):
    quoteObject = random.choice(QUOTELIST)
    if(quoteObject["said_by"] != ""):
        await ctx.send(sWrap(f'{ctx.author.name}: The quote: “{quoteObject["quote"]}”\nWas said by?', StringStyle.CYAN))
        reply = await bot.wait_for('message', check=check(ctx.author), timeout=30)
        if(testContent(reply.content, quoteObject['said_by'])): 
            addPoint(ctx.author.name)
            await ctx.send(sWrap(f'{reply.content}" is correctomundo!\nIt was said in which {quoteObject["genre"]}?',StringStyle.YELLOW))

        else: await ctx.send(sWrap(f'-{reply.content} is FAIL!\nBut, can you name the {quoteObject["genre"]}?' , StringStyle.DIFF))
    
    else:
        await ctx.send(sWrap(f'{ctx.author.name}: The quote: “{quoteObject["quote"]}”\nWas said in which {quoteObject["genre"]}?', StringStyle.CYAN))

    reply = await bot.wait_for('message', check=check(ctx.author), timeout=30)
    if(testContent(reply.content, quoteObject["where"])): 
        addPoint(ctx.author.name)
        await ctx.send(sWrap(reply.content+" is correctomundo!",StringStyle.YELLOW))
    else: 
        await ctx.send(sWrap(f'-{reply.content} is FAIL!!!' , StringStyle.DIFF))
    
    
    reply = await bot.wait_for('message', check=check(ctx.author), timeout=30)
    if(reply.content == "answer".lower()): 
        qNpcString = quoteObject["said_by"]
        if(qNpcString != ""): qNpcString = f'was said by accepted[{qNpcString}] and'
        await ctx.send(f'{quoteObject["quote"]} {qNpcString} is from the {quoteObject["genre"]} accepted[{quoteObject["where"]}]')


@bot.command(name='addquiz', help='can create quizes. Insert four strings for the  fields:quote, said_by, where, genre: example: !addquiz "A quote from a film" "The name of the actor" "the name of the  film" "genre"... \n'+
    'for multiple accepted answers you can write for said_by or where "dasBoot,das boot,das boots" These are then all accepted answers for the said_by field.')
async def addquiz(ctx, quote, said_by, where, genre):
   
    questions = {}
    questions["quote"] = quote
    questions["said_by"] = said_by
    questions["where"] = where
    questions["genre"] = genre
    questions["id"]= QUOTELIST[len(QUOTELIST)-1]["id"] + 1       
    await ctx.send(sWrap(f'{ctx.author.name}: You have inserted  The quote: “{questions["quote"]}”\n'+
        f'said by: [{questions["said_by"]}]\n'+
        f'from: [{questions["where"]}]\n'+
        f'genre: {questions["genre"]}\n'+
        f'Is this ok? Type "yes", any other response will cancel the request', StringStyle.CYAN))
    reply = await bot.wait_for('message', check=check(ctx.author), timeout=30)
    if(reply.content.lower() == "yes"):
        QUOTELIST.append(questions)
        with open("quotequiz.json.json", "w") as file:
            json.dump(QUOTELIST, file, indent=4)
        await ctx.send(sWrap(f'Great! You have entered a new quizset with id = {questions["id"]}. Thank you {ctx.author.name}!', StringStyle.CYAN))

@bot.command()
async def delQuiz(ctx, id):
    if(ctx.author.name != "DillDall"):
        await ctx.send(sWrap(f'{ctx.author.name}! You forget yourself, such actions are beyond you. You are not the great DillDall!', StringStyle.CYAN))
        return

    with open("quotequiz.json", "w") as file:
        for quote in QUOTELIST: 
            if(quote["id"] == int(id)):
                QUOTELIST.remove(quote)
                await ctx.send(sWrap(f'You sucessfully deleted the quote with id = {id}', StringStyle.CYAN))
                return
    await ctx.send(sWrap(f'-Quote with id = {id} not found in Quotelist', StringStyle.NONE))
        

@bot.command()
async def score(ctx):
    response="################SCORECARD##############################\n#\n#\n"
    leader = ""
    leaderScore = 0
    for player in SCORECARD:
        response += f'#     {player["name"]}: {player["score"]}\n'
        if(int(player["score"])>leaderScore):
            leader = player["name"]
            leaderScore = int(player["score"])

    await ctx.send(sWrap(f'{response}#\n#\n#   Guild quiz master is {leader}! with {leaderScore} points! Cheers!\n#\n######################################################', StringStyle.YELLOW)) 



@bot.command(name='roll', help='!roll 3d4 could give 3,1,2 = 6.. !roll 2d20 +3d10, could give "18,17=35 : 8,1,6=15 :  = 50"')
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


@bot.command(pass_context=True)
async def join(ctx):
    if ctx.message.author.voice:
        channel = ctx.message.author.voice.channel
        await channel.connect()

@bot.command(pass_context=True)
async def leave(ctx):
    guild = ctx.message.guild
    voice_client = guild.voice_client
    await voice_client.disconnect()

@bot.command(pass_context=True)
async def play(ctx, url):
    guild = ctx.message.guild
    voice_client = guild.voice_client
    player = await voice_client.create_ytdl_player(url)
    players[server.id] = player
    player.start()

bot.run(TOKEN)