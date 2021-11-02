import json
import random as rand

f = open("coins.json", encoding="utf8")
coins = json.load(f)

def getCoinID(arg):
    return list(filter(lambda x:x["Symbol"]==arg,coins))

# CoinGeckoAPI can only show rates against USD
# had to make a workaround for token-token rates
def crypto(cg, args):
    list = args.split(" ")
    if len(list) == 1:
        return "```Input a valid token!```"
    else:
        coin1 = list[1]
        coin1_ID = getCoinID(coin1.lower())[0]["Id"]
        result = cg.get_price(ids=coin1_ID, vs_currencies='usd')
        if len(list) > 2:
            coin2 = list[2]
            coin2_ID = getCoinID(coin2.lower())[0]["Id"]
            result2 = cg.get_price(ids=coin2_ID, vs_currencies='usd')
            print(result2)
            return "```" + coin1.upper() + "/" + coin2.upper() + " : " + str(result[coin1_ID]['usd']/result2[coin2_ID]['usd']) + "```"

        return "```" + coin1.upper() + "/USD : " + str(result[coin1_ID]['usd']) + "```"

def bepisMonke():
    num = rand.randint(0,1000)
    space = int(num/2) * " "
    if num < 69:
        return "||" + space + "bepis monke" + space + "||"
    elif num == 69:
        return "|| https://imgur.com/e54X8Pu ||" 

def seggs():
    num = rand.randint(0,1000)
    if num < 43:
        return "https://imgur.com/cZNc7Pl"