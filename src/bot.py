import asyncio
import json
import logging

import discord
from discord import app_commands
from discord.ext import commands

logger = logging.getLogger("discord")
logging.basicConfig(level=logging.WARNING)


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
    bot.tree.clear_commands()
    await bot.tree.sync()
    await load()
    await bot.start(bot_token)
    


@bot.tree.error
async def on_app_command_error(
    interaction: discord.Interaction, error: app_commands.AppCommandError
):
    if isinstance(error, discord.app_commands.TransformerError):
        error_message = f"The following time of **{error.value}** did not conform to the time format. It needs to be in 00:00.00 format"
        await interaction.response.send_message(f"{error_message}", ephemeral=True)


asyncio.run(main())
