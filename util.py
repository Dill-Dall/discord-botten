"""
A set of utility functions
"""

import enum

class StringStyle(enum.Enum):
    YELLOW = "fix"
    CYAN = "yaml"
    DIFF = "diff"
    NONE = ""

def sWrap(string, stringStyle):
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
