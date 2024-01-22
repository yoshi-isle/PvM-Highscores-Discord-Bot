import asyncio
import json

import discord
from discord.ext import commands
import logging

logger = logging.getLogger('discord')
logging.basicConfig(level=logging.DEBUG)


# Import keys
with open("../config/appsettings.local.json") as appsettings:
    data = json.load(appsettings)

bot_token = data["BotToken"]
channel_id = data["HighscoresChannelId"]

intents = discord.Intents.all()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    print("Online")


async def load():
    await bot.load_extension("bingo.bingo_cog")
    await bot.load_extension("hall_of_fame.hall_of_fame_cog")


async def main():
    await load()
    await bot.start(bot_token)
    await bot.tree.sync()


asyncio.run(main())
