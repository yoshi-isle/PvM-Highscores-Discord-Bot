import discord
import json
import embed_generator
import database
import constants.boss_names as boss_names
import constants.raid_names as raid_info
from discord.ext import commands

# Import keys
with open("../config/appsettings.local.json") as settings_json:
    data = json.load(settings_json)

bot_token = data["BotToken"]
channel_id = data["HighscoresChannelId"]

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())


@bot.command()
async def raidpbs(ctx):
    channel = ctx.channel
    await channel.purge()
    data = database.GetPersonalBests()

    for info in raid_info.RAID_INFO:
        await embed_generator.post_raids_embed(
            ctx,
            data,
            info,
            pb_categories=raid_info.RAID_INFO[info],
            number_of_placements=3,
        )


@bot.command()
async def bosspbs(ctx):
    channel = ctx.channel
    await channel.purge()
    data = database.GetPersonalBests()

    for info in raid_info.RAID_INFO:
        await embed_generator.post_raids_embed(
            ctx,
            data,
            info,
            pb_categories=raid_info.RAID_INFO[info],
            number_of_placements=3,
        )


bot.run(bot_token)
