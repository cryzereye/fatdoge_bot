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
"""
@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"
"""

# default triggers
@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith(command_prefix +'hello'):
        print(f'{message.author}')
        await message.channel.send('Hello!')

    if message.content.startswith(command_prefix +'bepis'):
        await message.channel.send('https://cdn.discordapp.com/emojis/804500782988525609.png?size=64')

    if message.content.startswith(command_prefix + 'crypto'):
        await message.channel.send(cc.crypto(cg , message.content))
    

TOKEN = open("module/token.txt","r")
client.run(TOKEN.readline()) 