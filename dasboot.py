# bot.py
from discord.ext import commands
bot = commands.Bot(command_prefix='!')

import os
import random 
import discord
import youtube_dl

import quiz
import diceroller

from dotenv import load_dotenv

import quotelist

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')


#SETUP
@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

@bot.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f'>>> Hi {member.name}, welcome to {GUILD}!'
    )


#QUIZ CONTROLLERS
@bot.command(name='99', help='Responds with a random quote from Brooklyn 99')
async def nine_nine(ctx):
    response = random.choice(quotelist.brooklyn_99_quotes)
    await ctx.send(response)

@bot.command()
async def avatar(ctx, member: discord.Member):
    show_avatar = discord.Embed(
        color = discord.Color.dark_blue()
    )
    show_avatar.set_image(url='{}'.format(member.avatar_url))
    await ctx.send(embed=show_avatar)


@bot.command(name='quiz', help='Starts a quiz about quotes.')
async def quiz_me(ctx):
    await quiz.quiz_me(bot, ctx)

@bot.command(name='addquiz', help='can create quizes. Insert four util.StringStyle for the  fields:quote, said_by, where, genre: example: !addquiz "A quote from a film" "The name of the actor" "the name of the  film" "genre"... \n'+
    'for multiple accepted answers you can write for said_by or where "dasBoot,das boot,das boots" These are then all accepted answers for the said_by field.')
async def addquiz(ctx, quote, said_by, where, genre):
    await quiz.addquiz(bot, ctx, quote, said_by, where, genre)

@bot.command(name='delQuiz', help='Delete quiz based on id')
async def delQuiz(ctx, id):
    await quiz.delQuiz(ctx,id)

@bot.command(name='score', help='Show scoreboard over quiz competitors')
async def score(ctx):
    await quiz.score(ctx)

@bot.command(name='roll', help='!roll 3d4 could give 3,1,2 = 6.. !roll 2d20 +3d10, could give "18,17=35 : 8,1,6=15 :  = 50"')
async def roll(ctx, *args):
    await  diceroller.roll(ctx, *args)



#TODO: MUSIC PLAYER
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