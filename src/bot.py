import discord
import json
import vardorvis
from discord.ext import commands

# Import keys
with open('../config/appsettings.local.json') as settingsJson:
    data = json.load(settingsJson)
BOT_TOKEN = data['BotToken']
CHANNEL_ID = data['HighscoresChannelId']

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

@bot.command()
async def updatehighscores(ctx):
    await vardorvis.Update(ctx)
    
bot.run(BOT_TOKEN)