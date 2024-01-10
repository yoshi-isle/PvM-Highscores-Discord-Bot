import discord
from discord import Embed
from discord import File
from discord.ext import commands, tasks
from dataclasses import dataclass
import datetime

# Prefill local values
BOT_TOKEN = "[Token goes here]"
CHANNEL_ID = 0

@dataclass
class Session:
    is_active: bool = False
    start_time: int = 0

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())
session = Session()

@bot.event
async def on_ready():
    print("Hello world")

@bot.command()
async def test(ctx):
    await ctx.send("Test")

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