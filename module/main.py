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
    print(f'{client.user.name} has joined Discord!')

# default triggers
@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('bepis'):
        await message.channel.send(cc.bepisMonke())

    if message.content.startswith('seggs'):
        await message.channel.send(cc.seggs())

    if message.content.startswith(command_prefix + 'crypto'):
        await message.channel.send(cc.crypto(cg , message.content))
    

TOKEN = open("module/token.txt","r")
client.run(TOKEN.readline()) 