import discord
import json
import bot_commands
from discord.ext import commands

# Import keys
with open("../config/appsettings.local.json") as settings_json:
    data = json.load(settings_json)

bot_token = data["BotToken"]
channel_id = data["HighscoresChannelId"]

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())


# Note - these commands are only for use if nothing exists in the channel yet
@bot.command()
async def createraidpbs(ctx):
    await bot_commands.create_raid_pbs(ctx)


@bot.command()
async def createbosspbs(ctx):
    await bot_commands.create_boss_pbs(ctx)


@bot.command()
async def updatebosspbs(ctx):
    await bot_commands.update_boss_pbs(ctx)


@bot.command()
async def updateraidspbs(ctx):
    await bot_commands.update_raids_pbs(ctx)


bot.run(bot_token)
