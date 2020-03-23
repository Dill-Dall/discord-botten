import enum

class StringStyle(enum.Enum):
   YELLOW= "fix"
   CYAN="yaml"
   DIFF="diff"
   NONE=""

def sWrap(string, stringStyle):
    return f""">>> ```{stringStyle.value}\n{string}```"""


def testContent(message, answer):
    answerList = answer.lower().split(",")
    if message.lower() in answerList: return True
    return False

def check(author):
    def inner_check(message):
        return message.author == author
    return inner_check