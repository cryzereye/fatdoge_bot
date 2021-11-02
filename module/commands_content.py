import json
import random as rand
import utilities as util

f = open("coins.json", encoding="utf8")
coins = json.load(f)

def getCoinID(arg):
    return list(filter(lambda x:x["Symbol"]==arg,coins))


# CoinGeckoAPI can only show rates against USD
# had to make a workaround for token-token rates
def crypto(cg, args, user):
    util.logger(str(user) + " queried " + args)
    try:
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
                return "```" + coin1.upper() + "/" + coin2.upper() + " : " + str(result[coin1_ID]['usd']/result2[coin2_ID]['usd']) + "```"

            return "```" + coin1.upper() + "/USD : " + str(result[coin1_ID]['usd']) + "```"
    except:
        return "```Input a valid token!```"

def bepisMonke(user):
    num = rand.randint(0,1000)

    util.logger(str(user) + " rolled " + str(num) + " in bepisMonke")

    space = int(num/2) * " "
    if num < 69:
        return "||" + space + "bepis monke" + space + "||"
    elif num == 69:
        return "|| https://imgur.com/e54X8Pu ||" 
    return ""

def seggs(user):
    num = rand.randint(0,1000)
    util.logger(str(user) + " rolled " + str(num) + " in seggs")
    if num < 43:
        return "https://imgur.com/cZNc7Pl"
    return ""