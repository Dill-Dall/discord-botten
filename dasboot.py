"""
A Discord bot.
"""

import os
import random

import discord
from discord.ext import commands
import youtube_dl
from dotenv import load_dotenv

import quiz
import diceroller
import quotelist

# bot.py
BOT = commands.Bot(command_prefix='!')
BOT.add_cog(diceroller.Diceroller(BOT))

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

#SETUP
@BOT.event
async def on_ready():
    print(f'{BOT.user.name} has connected to Discord!', flush=True)

@BOT.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f'>>> Hi {member.name}, welcome to {GUILD}!'
    )

#QUIZ CONTROLLERS
@BOT.command(name='99', help='Responds with a random quote from Brooklyn 99')
async def nine_nine(ctx):
    response = random.choice(quotelist.brooklyn_99_quotes)
    await ctx.send(response)

@BOT.command()
async def avatar(ctx, member: discord.Member):
    show_avatar = discord.Embed(
        color=discord.Color.dark_blue()
    )
    show_avatar.set_image(url='{}'.format(member.avatar_url))
    await ctx.send(embed=show_avatar)

@BOT.command(name='quiz', help='Starts a quiz about quotes.')
async def quiz_me(ctx):
    await quiz.quiz_me(BOT, ctx)

@BOT.command(name='addquiz', help='can create quizes. Insert four util.StringStyle for the  fields:quote, said_by, where, genre: example: !addquiz "A quote from a film" "The name of the actor" "the name of the  film" "genre"... \n'+
             'for multiple accepted answers you can write for said_by or where "dasBoot,das boot,das boots" These are then all accepted answers for the said_by field.')
async def add_quiz(ctx, quote, said_by, where, genre):
    await quiz.add_quiz(BOT, ctx, quote, said_by, where, genre)

@BOT.command(name='delquiz', help='Delete quiz based on id')
async def del_quiz(ctx, quiz_id):
    await quiz.del_quiz(ctx, quiz_id)

@BOT.command(name='score', help='Show scoreboard over quiz competitors')
async def score(ctx):
    await quiz.score(ctx)


#TODO: MUSIC PLAYER
PLAYERS = {}

@BOT.command(pass_context=True)
async def join(ctx):
    if ctx.message.author.voice:
        channel = ctx.message.author.voice.channel
        await channel.connect()

@BOT.command(pass_context=True)
async def leave(ctx):
    guild = ctx.message.guild
    voice_client = guild.voice_client
    await voice_client.disconnect()

@BOT.command(pass_context=True)
async def play(ctx, url):
    guild = ctx.message.guild
    voice_client = guild.voice_client
    player = await voice_client.create_ytdl_player(url)
    PLAYERS[server.id] = player
    player.start()

BOT.run(TOKEN)
