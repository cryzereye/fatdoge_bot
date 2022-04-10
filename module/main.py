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
config = cc.loadConfig()

# server status
@client.event
async def on_ready():
    game = discord.Game("with belly fats")
    await client.change_presence(activity = game)
    print("bot reporting")

# default triggers
@client.event
async def on_message(message):
    msg = ""
    if message.author == client.user:
        return

    if message.channel.id in config["allowed_channels"]:
        lowerMSG = message.content.lower()
        if message.content.startswith(command_prefix + 'price'):
            waitMsg = await message.channel.send("```Awaiting " + message.content + " response...```")
            msg = cc.crypto(cg , message.content, str(message.author))
            await waitMsg.edit(content = msg)
            return
        elif message.content.startswith(command_prefix +'lb'): 
            msg = cc.leaderboard(str(message.author), message.content)
        elif message.content.startswith(command_prefix +'winrate') or message.content.startswith(command_prefix +'wr'): 
            msg = cc.winrate(str(message.author))
        #elif str("bepis") in lowerMSG: 
        #    msg = cc.bepisMonke(str(message.author))
        elif str("seggs") in lowerMSG: 
            msg = cc.seggs(str(message.author))
        elif message.content.startswith(command_prefix +'whenmoon'):
            msg = cc.whenmoon()
        elif message.content.startswith(command_prefix +'p2p'):
            msg = cc.p2p()
    
    if message.content.startswith(command_prefix + 'gagofy') and message.channel.id == 806838914806710282:
        msg = cc.gagofy(str(message.author))
    elif message.content.startswith(command_prefix + 'help'):
        msg = cc.help(str(message.author))

    if (msg != ""): await message.channel.send(msg)
    
TOKEN = open("module/token.txt","r")
client.run(TOKEN.readline()) 