from genericpath import exists
from http.client import ResponseNotReady
import json, requests
from pickle import TRUE
import random as rand
import utilities as util
from datetime import datetime
from binance.spot import Spot

FIXERIOFXAPI_URL = "http://data.fixer.io/api/latest?access_key=419f3befde9b7e362bc748d9c767a966&symbols=USD,PHP,JPY,RUB,KRW&format=1"
P2PAPI_URL = "https://p2p.binance.com/bapi/c2c/v2/friendly/c2c/adv/search"

# CoinGeckoAPI coins list
coins = {}
while coins == {}:
    coins = requests.get("https://api.coingecko.com/api/v3/coins/list").json()

with open("json\\bepisLB.json", "r") as bepisLB_file:
    bepisLB = json.load(bepisLB_file)
    bepisLB_file.close()

with open("json\\seggsLB.json", "r") as seggsLB_file:
    seggsLB = json.load(seggsLB_file)
    seggsLB_file.close()

with open("json\\gagofy.json", "r") as gagofy_file:
    gagofyData = json.load(gagofy_file)
    gagofy_file.close()

with open("json\\mooncycle.json", "r") as moon_file:
    moonData = json.load(moon_file)
    moon_file.close()

def gwei(user, cfg):
    s = "```"
    for x in range(0, len(cfg)):
        r = requests.get(
        "https://api." + str(cfg[x]["name"]) + "scan."+ str(cfg[x]["suffix"]) +"/api?module=gastracker&action=gasoracle&apikey=" + str(cfg[x]["key"]))
        if r.status_code == 200:
            s += ("From "+ str(cfg[x]["name"]).capitalize() +"scan."+str(cfg[x]["suffix"])+":\n\n"
            "Low :\t" + r.json()["result"]["SafeGasPrice"] + "\n"
            "Ave :\t" + r.json()["result"]["ProposeGasPrice"] + "\n"
            "High:\t" + r.json()["result"]["FastGasPrice"] + "\n\n\n")
        else:
            s += cfg[x]["name"] + "Gas prices not available"
    return s + "```"

def echo(user, channel):
    util.logger(str(user) + " used echo")
    print ("" + str(channel))
    return ""

def persy(user):
    util.logger(str(user) + " used gspot")
    return "pakyu " + user.mention + " wag kang bastos >:("

def tenor(key, user, s):
    util.logger(str(user) + " used tenor for " + s)
    r = requests.get(
    "https://g.tenor.com/v1/random?q=%s&key=%s&limit=%s&locale=en_US&media_filter=minimal&contentfilter=medium" % (s, key, 1))

    if r.status_code == 200:
        return r.json()["results"][0]["media"][0]["gif"]["url"]
    else:
        return None

def spot(pair, k, s, user):
    util.logger(str(user) + " used spot for " + pair)
    bin_client = Spot(key=k, secret=s)
    s = "```From Binance Spot:\n\n"
    if str(pair) == "ALL":
        watchlist = [
            "BTCUSDT",
            "ETHUSDT",
            "LRCUSDT",
            "ADAUSDT",
            "LUNABUSD",
            "IMXUSDT"
        ]
        
        for x in range(0, len(watchlist)):
            res = bin_client.ticker_price(watchlist[x])
            s += "" + watchlist[x] + ":\t" + res["price"] + "\n"
    else:
        res = bin_client.ticker_price(pair)
        s += "" + pair + ":\t" + res["price"] + "\n"

    return s + "```"


def fx(user):
    util.logger(str(user) + " used fx")
    response = requests.get(FIXERIOFXAPI_URL) 
    s = ("```"
    "from: data.fixer.io/api\n\n"
    "PHP/USD:\t" + str(float(response.json()["rates"]["PHP"])/float(response.json()["rates"]["USD"])) + "\n"
    "PHP/EUR:\t" + str(response.json()["rates"]["PHP"]) + "\n"
    "PHP/JPY:\t" + str(float(response.json()["rates"]["PHP"])/float(response.json()["rates"]["JPY"])) + "\n"
    "PHP/RUB:\t" + str(float(response.json()["rates"]["PHP"])/float(response.json()["rates"]["RUB"])) + "\n"
    "PHP/KRW:\t" + str(float(response.json()["rates"]["PHP"])/float(response.json()["rates"]["KRW"])) + "\n"
    "```")
    return s

# allows user to get notified when Binance P2P PHP/USDT rate crosses inputted rate
# 5 secs refresh: to be implemented
def p2pnotify(user, msg):
    try:
        list = msg.split(" ")
        rate = float(list[2])
        return "<@" + str(user) + "> will be notified once PHP/USDT P2P buy rate is below or equal to " + str(f'{rate:0.2f}')
    except:
        return "Invalid p2p notify command! Please check rate inputted!"
    
# returns 1 Binance P2P USDT/PHP result with the lowest buying rate
def p2p(tradeType, payMethod, user):
    util.logger(str(user) + " used p2p for " + tradeType)
    data = {
        "asset": "USDT",
        "fiat": "PHP",
        "merchantCheck": True,
        "page": 1,
        "publisherType": "merchant",
        "rows": 5,
        "tradeType": tradeType,
    }

    if payMethod != "":
        data.update({"payTypes": [payMethod]})

    try:
        response = requests.post(P2PAPI_URL, json=data)
        r_data = response.json()
        if len(r_data["data"]) == 0:
            raise Exception
    except:
        s = ("```Invalid p2p options entered!\n\n"
            "p2p (buy|sell) (gcash|ing|bank|ubop)"
            "```"
        )
        return s

    s = "```Binance P2P PHP/USDT " +  tradeType
    if payMethod != "":
        s += " for pay method " + payMethod
    s += "\n\n"

    i = 0
    for x in r_data["data"]:
        payMethods = ""
        for y in r_data["data"][i]["adv"]["tradeMethods"]:
            payMethods += str(y["identifier"]) + " "

        s += (
            "Binance P2P PHP/USDT:   " + str(r_data["data"][i]["adv"]["price"]) + "\n"
            "Available USDT:         " + str(r_data["data"][i]["adv"]["surplusAmount"]) + "\n"
            "Merchant Name:          " + str(r_data["data"][i]["advertiser"]["nickName"]) + "\n"
            "Payment methods:        " + payMethods + "\n"
            "================================================\n\n"
        )
        i+=1

    s += "```"

    return s

# return next new moon and full moon dates
# from manual list fetched from "https://www.timeanddate.com/moon/phases/@220244"
def whenmoon(user):
    util.logger(str(user) + " used whenmoon")
    currentDate = datetime.today()
    loopDate = currentDate
    fullMoonSTR = ""
    newMoonSTR = ""

    for x in moonData["fullmoons"]:
        prevFullMoon = datetime.strftime(loopDate, '%B %d %Y')
        loopDate = datetime.strptime(x, '%d/%m/%Y')
        if currentDate < loopDate:
            fullMoonSTR = datetime.strftime(loopDate, '%B %d %Y')
            break
    
    for x in moonData["newmoons"]:
        prevNewMoon = datetime.strftime(loopDate, '%B %d %Y')
        loopDate = datetime.strptime(x, '%d/%m/%Y')
        if currentDate < loopDate:
            newMoonSTR = datetime.strftime(loopDate, '%B %d %Y')
            break
    s = ("```" +
    "\nPrev FULL moon:  " + prevFullMoon +
    "\nNext FULL moon:  " + fullMoonSTR +
    "\nPrev NEW moon:   " + prevNewMoon +
    "\nNext NEW moon:   " + newMoonSTR +
    "```")
    return s

# CoinGeckoAPI can only show rates against USD
# had to make a workaround for token-token rates
def crypto(cg, args, user):
    util.logger(str(user) + " queried " + args)
    result = {}
    result2 = {}
    s = "```From CoinGecko:\n\n"
    try:
        list = args.split(" ")
        if len(list) == 1:
            return "```Input a valid token!```"
        else:
            coin1 = list[1]
            coin1_ID = util.getCoinID(coin1.lower(), coins)[0]["id"]
            while result == {}:
                try:
                    result = cg.get_price(ids=coin1_ID, vs_currencies='usd')
                except:
                    pass
            if len(list) > 2:
                coin2 = list[2]
                coin2_ID = util.getCoinID(coin2.lower(), coins)[0]["id"]
                while result2 == {}:
                    try:
                        result2 = cg.get_price(ids=coin2_ID, vs_currencies='usd')
                    except:
                        pass
                s += ""+ coin1_ID + "/" + coin2_ID + "  " + coin1.upper() + "/" + coin2.upper() + " : " + str(result[coin1_ID]['usd']/result2[coin2_ID]['usd'])

            else:
                s += "" + coin1_ID + "  " + coin1.upper() + "/USD : " + str(result[coin1_ID]['usd'])
    except:
        return "```Input a valid token!```"
    return s + "```"

def help(user):
    util.logger(str(user) + " queried help")
    s = ("```AVAILABLE COMMANDS:\n"
            "only in #bot-spam and #crypto:\n"
            "^spot [binance pairing ex: BTCUSDT]\n"
            "^fx\n"
            "^p2p [buy|sell [gcash|ubop|bank|ing|others...]]\n"
            "^price coin1 [coin2: default is USD]\n"
            "^gwei\n\n"
            "only in #degeneral:\n"
            "^gagofy\n"
            "\n\n"
            "required = ()\n"
            "optional = []\n"
            "```"
        )
    return s

def gagofy(user):
    util.logger(str(user) + " queried gagofy")
    length = len(gagofyData["statements"])
    randNum = rand.randint(0, length - 1)
    return gagofyData["statements"][randNum]