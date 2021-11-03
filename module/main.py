#large
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
command_prefix='!'
bot = commands.Bot(command_prefix)
client = discord.Client(intents = intents)

# server status
@client.event
async def on_ready():
    print("monke reporting".format(client))

# default triggers
@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('bepis') and message.channel.id in (806838914806710282, 746603176421097514): #RMI-KB degeneral, test server
        msg = cc.bepisMonke(str(message.author))
        if (msg != ""): await message.channel.send(msg)

    if message.content.startswith('seggs') and message.channel.id in (806838914806710282, 746603176421097514): #RMI-KB degeneral, test server
        msg = cc.seggs(str(message.author))
        if (msg != ""): await message.channel.send(msg)

    if message.content.startswith(command_prefix +'lb') and message.channel.id in (806838914806710282, 746603176421097514): #RMI-KB degeneral, test server
        msg = cc.leaderboard(str(message.author), message.content)
        if (msg != ""): await message.channel.send(msg)

    if message.content.startswith(command_prefix +'winrate') and message.channel.id in (806838914806710282, 746603176421097514): #RMI-KB degeneral, test server
        msg = cc.winrate(str(message.author), message.content)
        if (msg != ""): await message.channel.send(msg)

    if message.content.startswith(command_prefix + 'price') and message.channel.id in (816515392809730049, 746603176421097514): #RMI-KB crypto, test server
        msg = cc.crypto(cg , message.content, str(message.author))
        if (msg != ""): await message.channel.send(msg)
    

TOKEN = open("module/token.txt","r")
client.run(TOKEN.readline()) 