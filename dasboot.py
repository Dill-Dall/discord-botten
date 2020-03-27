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
import music

import quotelist
import util


# bot.py
BOT = commands.Bot(command_prefix='!')
BOT.add_cog(diceroller.Diceroller(BOT))
BOT.add_cog(quiz.Quiz(BOT))
BOT.add_cog(music.Music(BOT))

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

#QUIZ CONTROLLERS

@BOT.command(name='countdown', help='Do a countdown')
async def countdown(ctx, countdown):
    await util.timer(ctx, countdown)




BOT.run(TOKEN)
