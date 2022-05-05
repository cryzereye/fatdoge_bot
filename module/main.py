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
        #elif message.content.startswith(command_prefix +'lb'): 
        #    msg = cc.leaderboard(str(message.author), message.content)
        #elif message.content.startswith(command_prefix +'winrate') or message.content.startswith(command_prefix +'wr'): 
        #    msg = cc.winrate(str(message.author))
        #elif str("bepis") in lowerMSG: 
        #    msg = cc.bepisMonke(str(message.author))
        #elif str("seggs") in lowerMSG: 
        #    msg = cc.seggs(str(message.author))
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

    # for RMI degeneral only
    if message.channel.id == 806838914806710282:
        if message.content.startswith(command_prefix + 'gagofy'):
            msg = cc.gagofy(str(message.author))
        elif message.content.startswith(command_prefix +'angry'):
            msg = cc.angry(config["tnrky"], str(message.author))
        elif message.content.startswith(command_prefix +'kilig'):
            msg = cc.kilig(config["tnrky"], str(message.author))

    if (msg != ""): await message.channel.send(msg)

client.run(config["token"])