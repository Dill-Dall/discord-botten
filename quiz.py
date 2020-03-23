import json
import random

import util


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
                return
        player = {}
        player["name"] = name
        player["score"] = 1
        player["id"]= SCORECARD[len(SCORECARD)-1]["id"] + 1
        SCORECARD.append(player)
        json.dump(SCORECARD, file, indent=4)    
    

async def quiz_me(bot,ctx):
    quoteObject = random.choice(QUOTELIST)
    if(quoteObject["said_by"] != ""):
        await ctx.send(util.sWrap(f'{ctx.author.name}: The quote: “{quoteObject["quote"]}”\nWas said by?', util.StringStyle.CYAN))
        reply = await bot.wait_for('message', check=util.check(ctx.author), timeout=30)
        if(util.testContent(reply.content, quoteObject['said_by'])): 
            addPoint(ctx.author.name)
            await ctx.send(util.sWrap(f'{reply.content} is correctomundo!\nIt was said in which {quoteObject["genre"]}?',util.StringStyle.YELLOW))

        else: await ctx.send(util.sWrap(f'-{reply.content} is FAIL!\nBut, can you name the {quoteObject["genre"]}?' , util.StringStyle.DIFF))
    
    else:
        await ctx.send(util.sWrap(f'{ctx.author.name}: The quote: “{quoteObject["quote"]}”\nWas said in which {quoteObject["genre"]}?', util.StringStyle.CYAN))

    reply = await bot.wait_for('message', check=util.check(ctx.author), timeout=30)
    if(util.testContent(reply.content, quoteObject["where"])): 
        addPoint(ctx.author.name)
        await ctx.send(util.sWrap(reply.content+" is correctomundo!",util.StringStyle.YELLOW))
    else: 
        await ctx.send(util.sWrap(f'-{reply.content} is FAIL!!!' , util.StringStyle.DIFF))
    
    
    reply = await bot.wait_for('message', check=util.check(ctx.author), timeout=30)
    if(reply.content == "answer".lower()): 
        qNpcString = quoteObject["said_by"]
        if(qNpcString != ""): qNpcString = f'was said by accepted[{qNpcString}] and'
        await ctx.send(f'{quoteObject["quote"]} {qNpcString} is from the {quoteObject["genre"]} accepted[{quoteObject["where"]}]')

async def addquiz(bot, ctx, quote, said_by, where, genre):
    questions = {}
    questions["quote"] = quote
    questions["said_by"] = said_by
    questions["where"] = where
    questions["genre"] = genre
    questions["id"]= QUOTELIST[len(QUOTELIST)-1]["id"] + 1       
    await ctx.send(util.sWrap(f'{ctx.author.name}: You have inserted  The quote: “{questions["quote"]}”\n'+
        f'said by: [{questions["said_by"]}]\n'+
        f'from: [{questions["where"]}]\n'+
        f'genre: {questions["genre"]}\n'+
        f'Is this ok? Type "yes", any other response will cancel the request', util.StringStyle.CYAN))
    reply = await bot.wait_for('message', check=util.check(ctx.author), timeout=30)
    if(reply.content.lower() == "yes"):
        QUOTELIST.append(questions)
        with open("quotequiz.json", "w") as file:
            json.dump(QUOTELIST, file, indent=4)
        await ctx.send(util.sWrap(f'Great! You have entered a new quizset with id = {questions["id"]}. Thank you {ctx.author.name}!', util.StringStyle.CYAN))

async def delQuiz(ctx, id):
    if(ctx.author.name != "DillDall"):
        await ctx.send(util.sWrap(f'{ctx.author.name}! You forget yourself, such actions are beyond you. You are not the great DillDall!', util.StringStyle.CYAN))
        return
    with open("quotequiz.json", "w") as file:
        for quote in QUOTELIST: 
            if(quote["id"] == int(id)):
                QUOTELIST.remove(quote)
                await ctx.send(util.sWrap(f'You sucessfully deleted the quote with id = {id}', util.StringStyle.CYAN))
                json.dump(QUOTELIST, file, indent=4)
                return
    await ctx.send(util.sWrap(f'-Quote with id = {id} not found in Quotelist', util.StringStyle.NONE))
        

async def score(ctx):
    response="################SCORECARD##############################\n#\n#\n"
    leader = ""
    leaderScore = 0
    for player in SCORECARD:
        response += f'#     {player["name"]}: {player["score"]}\n'
        if(int(player["score"])>leaderScore):
            leader = player["name"]
            leaderScore = int(player["score"])

    await ctx.send(util.sWrap(f'{response}#\n#\n#   Guild quiz master is {leader}! with {leaderScore} points! Cheers!\n#'+
    '\n########################################################', util.StringStyle.YELLOW)) 
