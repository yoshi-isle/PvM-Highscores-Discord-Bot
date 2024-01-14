import discord
import json
import vardorvis
import database
from discord.ext import commands

# Import keys
with open('../config/appsettings.local.json') as settings_json:
    data = json.load(settings_json)

BOT_TOKEN = data['BotToken']
CHANNEL_ID = data['HighscoresChannelId']

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

@bot.command()
async def updatehighscores(ctx):
    # Load data
    data = database.GetPersonalBests()

    # Post ToA PBs
    # Post ToB PBs
    # Post CoX PBs
    # Post Nightmare PBs
    # Post DT2 bosses
    await vardorvis.post_embed(ctx, data)

print("Bot running")
bot.run(BOT_TOKEN)