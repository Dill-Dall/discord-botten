"""
A set of utility functions
"""

import enum
import time
import sys

class StringStyle(enum.Enum):
    YELLOW = "fix"
    CYAN = "yaml"
    DIFF = "diff"
    NONE = ""

def sWrap(string, stringStyle = StringStyle.NONE):
    return f""">>> ```{stringStyle.value}\n{string}```"""


def testContent(message, answer):
    answer_list = answer.lower().split(",")
    if message.lower() in answer_list: 
        return True
    return False

def check(author):
    def inner_check(message):
        return message.author == author
    return inner_check

#Should be able to combine with check in a clean way
def checkBot(author, bot):
    def inner_check(message):
        return message.author != bot
    return inner_check

async def timer(ctx, countdown):
    msg = await ctx.send(f'Timer: {countdown}')

    for remaining in range(int(countdown), 0, -1):
        start_time = time.time()
        await msg.edit(content=f'Timer: {remaining}')
        current_time = time.time()
        elapsed_time = current_time - start_time
        if(1-elapsed_time  > 0):
            time.sleep(1-elapsed_time)

