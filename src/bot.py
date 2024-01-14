import discord
import json
import vardorvis
import database
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

database.testgetdata()
print("Bot running")
bot.run(BOT_TOKEN)