#large
from discord import activity
import discord
from discord.ext import commands
from pycoingecko import CoinGeckoAPI

#local
import commands_content as cc
import utilities as util

#packages
cg = CoinGeckoAPI()

#permissions
intents = discord.Intents.default()
intents.typing = True

#config load
config = util.loadConfig()
command_prefix = config["command_prefix"]

#general bot setup
bot = commands.Bot(command_prefix)
client = discord.Client(intents = intents)

# server status
@client.event
async def on_ready():
    game = discord.Game("^help")
    await client.change_presence(activity = game)
    print("bot reporting")

# default triggers
@client.event
async def on_message(message):
    msg = ""
    if message.author == client.user: #filter out bot messages
        return

    # all channels
    if message.content.startswith(command_prefix + 'help'):
            msg = cc.help(str(message.author))

    if message.channel.id in config["allowed_channels"]:
        lowerMSG = message.content.lower()
        options = ""
        if message.content.startswith(command_prefix + 'price'):
            waitMsg = await message.channel.send("```Awaiting " + message.content + " response...```")
            msg = cc.crypto(cg , message.content, str(message.author))
            await waitMsg.edit(content = msg)
            return
        elif message.content.startswith(command_prefix +'spot'):
            try:
                options = message.content.split(" ")[1]
            except:
                options = "all"
            msg = cc.spot(options, config["bikey"], config["s"], str(message.author))
        elif message.content.startswith(command_prefix +'whenmoon'):
            msg = cc.whenmoon(str(message.author))
        elif message.content.startswith(command_prefix +'p2p'):
            if message.content.startswith(command_prefix +'p2p notify'):
                msg = cc.p2pnotify(str(message.author.id), message.content)
            elif message.content.startswith(command_prefix +'p2p buy'): # dirty fast workaround below
                try:
                    msg = cc.p2p('BUY', message.content.split(" ")[2], str(message.author))
                except:
                    msg = cc.p2p('BUY', "", str(message.author))
            elif message.content.startswith(command_prefix +'p2p sell'):
                try:
                    msg = cc.p2p('SELL', message.content.split(" ")[2], str(message.author))
                except:
                    msg = cc.p2p('SELL', "", str(message.author))
            else:
                try:
                    msg = cc.p2p('BUY', message.content.split(" ")[1], str(message.author))
                except:
                    msg = cc.p2p('BUY',"", str(message.author))
        elif message.content.startswith(command_prefix +'fx'):
            msg = cc.fx(str(message.author))
        elif message.content.startswith(command_prefix +'gspot'):
            msg = cc.persy(message.author)
        elif message.content.startswith(command_prefix +'echo'):
            try:
                msg = cc.echo(str(message.author), message.content.split(" ")[1])
            except:
                msg = cc.echo(str(message.author), "")
        elif message.content.startswith(command_prefix +'gwei'):
            msg = cc.gwei(str(message.author), config["ethscan"])

    # for RMI degeneral only
    if message.channel.id == 806838914806710282:
        if message.content.startswith(command_prefix + 'gagofy'):
            msg = cc.gagofy(str(message.author))
        elif message.content.startswith(command_prefix +'tenor'):
            try: 
                msg = cc.tenor(config["tnrky"], str(message.author), message.content.split(" ")[1])
            except:
                msg = cc.tenor(config["tnrky"], str(message.author), "confused")

    if (msg != ""): await message.channel.send(msg)

client.run(config["token"])