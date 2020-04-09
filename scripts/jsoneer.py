import json
import quotelist

##Clean file 

#with open("quotequiz.json", "r") as file:
 #   QUOTELIST = json.load(file)

#with open("quotequiz.json", "w") as file:
#    i = 0 
#    for quote in QUOTELIST:
#        i = i+1
#        quote["id"] = i
#
#
#    json.dump(QUOTELIST, file, indent=4)
#


with open("quotequiz.json", "w") as file:
    i = 0 
    quote_list = []
    for quote in quotelist.quoteObjectList:
        questions = {}
        questions["quote"] = quote.quote
        questions["said_by"] = quote.npc
        questions["where"] = quote.game
        questions["genre"] = "game"
        i = i+1
        questions["id"] = i
        quote_list.append(questions)
    json.dump(quote_list, file, indent=4)
