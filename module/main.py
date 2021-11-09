#large
from discord import activity
from flask import Flask
import discord
from discord.ext import commands
from pycoingecko import CoinGeckoAPI

#local
import commands_content as cc

#packages
app = Flask(__name__)
cg = CoinGeckoAPI()

#permissions
intents = discord.Intents.default()
intents.typing = True

#general bot setup
command_prefix='^'
bot = commands.Bot(command_prefix)
client = discord.Client(intents = intents)

# server status
@client.event
async def on_ready():
    #status = discord.Activity(name = "bepis monke", state = "bepis monke", details = "bepis monke")
    gameOjb = discord.Game("MONKE with bepis")
    print("monke reporting".format(client))
    await client.change_presence(activity = gameOjb)

# default triggers
@client.event
async def on_message(message):
    if message.author == client.user:
        return

    lowerMSG = message.content.lower()

    if message.content.startswith(command_prefix +'lb') and message.channel.id in (746603176421097514, 793865181289512961): # test server, RMI bot spam
        msg = cc.leaderboard(str(message.author), message.content)
        if (msg != ""): await message.channel.send(msg)

    elif message.content.startswith(command_prefix +'winrate') and message.channel.id in ( 746603176421097514, 793865181289512961): #test server, RMI bot spam
        msg = cc.winrate(str(message.author), message.content)
        if (msg != ""): await message.channel.send(msg)

    elif message.content.startswith(command_prefix + 'price') and message.channel.id in (816515392809730049, 746603176421097514, 793865181289512961): #RMI-KB crypto, test server, RMI bot spam
        msg = cc.crypto(cg , message.content, str(message.author))
        if (msg != ""): await message.channel.send(msg)

    elif message.content.startswith(command_prefix + 'help') and message.channel.id in (816515392809730049, 746603176421097514, 793865181289512961): #RMI-KB crypto, test server, RMI-KB degeneral, RMI bot spam
        msg = cc.help()
        if (msg != ""): await message.channel.send(msg)

    elif str("bepis") in lowerMSG and message.channel.id in (746603176421097514, 793865181289512961): # test server, RMI bot spam
        msg = cc.bepisMonke(str(message.author))
        if (msg != ""): await message.channel.send(msg)

    elif str("seggs") in lowerMSG and message.channel.id in (746603176421097514, 793865181289512961): # test server, RMI bot spam
        msg = cc.seggs(str(message.author))
        if (msg != ""): await message.channel.send(msg)

    

TOKEN = open("module/token.txt","r")
client.run(TOKEN.readline()) 