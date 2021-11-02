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

    if message.content.startswith('bepis'):
        msg = cc.bepisMonke(message.author)
        if (msg != ""): await message.channel.send(msg)

    if message.content.startswith('seggs'):
        msg = cc.seggs(message.author)
        if (msg != ""): await message.channel.send(msg)

    if message.content.startswith(command_prefix + 'crypto'):
        msg = cc.crypto(cg , message.content, message.author)
        if (msg != ""): await message.channel.send(msg)
    

TOKEN = open("module/token.txt","r")
client.run(TOKEN.readline()) 