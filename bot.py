import discord
from discord import Embed
from discord import File
from discord.ext import commands, tasks
from dataclasses import dataclass
import json

# Import keys
with open('appsettings.local.json') as json:
    data = json.load(json)
BOT_TOKEN = data['BotToken']
CHANNEL_ID = data['HighscoresChannelId']

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

@bot.command()
async def updatehighscores(ctx):
    embed = Embed(title="Vardorvis", color=0xFF1E6D)
    embed.add_field(
        name="",
        value=":first_place:  Kitty Neko - 0:36\n :second_place:  Yoshe - 0:48\n :third_place:  Xavierman73 - 2:56",
        inline=False
    )
    image_path = "vardorvis.png"
    with open(image_path, "rb") as image_file:
        image = File(image_file)
    embed.set_thumbnail(url="attachment://vardorvis.png")

    await ctx.send(file=image, embed=embed)

bot.run(BOT_TOKEN)