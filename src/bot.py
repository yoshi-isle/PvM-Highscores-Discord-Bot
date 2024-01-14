import discord
import json
import embeds.vardorvis
import database
from discord.ext import commands

# Import keys
with open('../config/appsettings.local.json') as settings_json:
    data = json.load(settings_json)

bot_token = data['BotToken']
channel_id = data['HighscoresChannelId']

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
    await embeds.vardorvis.post_embed(ctx, data)

print("Bot running")
bot.run(bot_token)