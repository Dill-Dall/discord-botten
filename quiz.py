"""
Module to handle stuff related to quiz
"""

import json
import random
import asyncio

import util


with open("quotequiz.json", "r") as file:
    QUOTELIST = json.load(file)

with open("score.json", "r") as file:
    SCORECARD = json.load(file)


def add_point(name):
    with open("score.json", "w") as file:
        for player in SCORECARD:
            if player["name"] == name:
                player["score"] = str(int(player["score"]) + 1)
                json.dump(SCORECARD, file, indent=4)
                return
        new_player = {}
        new_player["name"] = name
        new_player["score"] = 1
        new_player["id"] = SCORECARD[len(SCORECARD)-1]["id"] + 1
        SCORECARD.append(new_player)
        json.dump(SCORECARD, file, indent=4)


async def quiz_me(bot, ctx):
    quote_object = random.choice(QUOTELIST)
    if quote_object["said_by"] != "":
        await ctx.send(util.sWrap(f'{ctx.author.name}: The quote: “{quote_object["quote"]}” (id: {quote_object["id"]})\nWas said by?', util.StringStyle.CYAN))
        try:
            reply = await bot.wait_for('message', check=util.check(ctx.author), timeout=30)
        except asyncio.TimeoutError:
            await ctx.send(util.sWrap(f'You were too slow!\nBut, can you name the {quote_object["genre"]}?', util.StringStyle.DIFF))
        else:
            if util.testContent(reply.content, quote_object['said_by']):
                add_point(ctx.author.name)
                await ctx.send(util.sWrap(f'{reply.content} is correctomundo!\nIt was said in which {quote_object["genre"]}?', util.StringStyle.YELLOW))

            else: await ctx.send(util.sWrap(f'-{reply.content} is FAIL!\nBut, can you name the {quote_object["genre"]}?', util.StringStyle.DIFF))

    else:
        await ctx.send(util.sWrap(f'{ctx.author.name}: The quote: “{quote_object["quote"]}” (id: {quote_object["id"]})\nWas said in which {quote_object["genre"]}?', util.StringStyle.CYAN))

    try:
        reply = await bot.wait_for('message', check=util.check(ctx.author), timeout=30)
    except asyncio.TimeoutError:
        await ctx.send(util.sWrap("You were too slow, try again!", util.StringStyle.DIFF))
    else:
        if util.testContent(reply.content, quote_object["where"]):
            add_point(ctx.author.name)
            await ctx.send(util.sWrap(reply.content+" is correctomundo!", util.StringStyle.YELLOW))
        else:
            await ctx.send(util.sWrap(f'-{reply.content} is FAIL!!!', util.StringStyle.DIFF))

    reply = await bot.wait_for('message', check=util.check(ctx.author), timeout=30)
    if reply.content == "answer".lower():
        q_npc_string = quote_object["said_by"]
        if q_npc_string != "":
            q_npc_string = f'was said by accepted[{q_npc_string}] and'
        await ctx.send(f'{quote_object["quote"]} {q_npc_string} is from the {quote_object["genre"]} accepted[{quote_object["where"]}]')


async def add_quiz(bot, ctx, quote, said_by, where, genre):
    questions = {}
    questions["quote"] = quote
    questions["said_by"] = said_by
    questions["where"] = where
    questions["genre"] = genre
    questions["id"] = QUOTELIST[len(QUOTELIST)-1]["id"] + 1
    await ctx.send(util.sWrap(f'{ctx.author.name}: You have inserted  The quote: “{questions["quote"]}”\n'
                              + f'said by: [{questions["said_by"]}]\n'
                              + f'from: [{questions["where"]}]\n'
                              + f'genre: {questions["genre"]}\n'
                              + f'Is this ok?'
                              + f'Type "yes", any other response will cancel the request', util.StringStyle.CYAN))
    reply = await bot.wait_for('message', check=util.check(ctx.author), timeout=30)
    if reply.content.lower() == "yes":
        QUOTELIST.append(questions)
        with open("quotequiz.json", "w") as file:
            json.dump(QUOTELIST, file, indent=4)
        await ctx.send(util.sWrap(f'Great! You have entered a new quizset with id = {questions["id"]}. Thank you {ctx.author.name}!', util.StringStyle.CYAN))

async def del_quiz(ctx, quiz_id):
    if ctx.author.name != "DillDall":
        await ctx.send(util.sWrap(f'{ctx.author.name}! You forget yourself, such actions are beyond you. You are not the great DillDall!', util.StringStyle.CYAN))
        return
    with open("quotequiz.json", "w") as file:
        for quote in QUOTELIST:
            if quote["id"] == int(quiz_id):
                QUOTELIST.remove(quote)
                await ctx.send(util.sWrap(f'You sucessfully deleted the quote with id = {quiz_id}', util.StringStyle.CYAN))
                json.dump(QUOTELIST, file, indent=4)
                return
    await ctx.send(util.sWrap(f'-Quote with id = {quiz_id} not found in Quotelist', util.StringStyle.NONE))


async def score(ctx):
    response = "################SCORECARD##############################\n#\n#\n"
    leader = ""
    leader_score = 0
    for player in SCORECARD:
        response += f'#     {player["name"]}: {player["score"]}\n'
        if int(player["score"]) > leader_score:
            leader = player["name"]
            leader_score = int(player["score"])

    await ctx.send(util.sWrap(f'{response}#\n#\n#   Guild quiz master is {leader}! with {leader_score} points! Cheers!\n#'
                              + '\n########################################################', util.StringStyle.YELLOW))
