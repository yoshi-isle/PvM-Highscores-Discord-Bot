import discord
import json
import embed_generator
import database
import constants.boss_names as boss_names
import constants.pvm_enums as pvm_enums
import constants.raid_names as raid_info
from discord.ext import commands
from discord import Interaction, SelectOption, ButtonStyle
from enum import Enum

# Import keys
with open("../config/appsettings.local.json") as appsettings:
    data = json.load(appsettings)

bot_token = data["BotToken"]
channel_id = data["HighscoresChannelId"]

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

BossName = Enum(
    "BossName",
    [
        "NIGHTMARE_SOLO",
        "PHOSANIS_NIGHTMARE",
        "VARDORVIS",
        "DUKE_SUCELLUS",
        "THE_WHISPERER",
        "LEVIATHAN",
        "VARDORVIS_AWAKENED",
        "DUKE_SUCELLUS_AWAKENED",
        "THE_WHISPERER_AWAKENED",
        "LEVIATHAN_AWAKENED",
        "INFERNO",
        "FIGHT_CAVES",
        "THE_GAUNTLET",
        "THE_CORRUPTED_GAUNTLET",
        "ZULRAH",
        "VORKATH",
        "GROTESQUE_GUARDIANS",
        "ALCHEMICAL_HYDRA",
        "PHANTOM_MUSPAH",
        "HESPORI",
        "MIMIC",
        "HALLOWED_SEPULCHRE",
    ],
)


@bot.event
async def on_ready():
    await bot.tree.sync()


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

    for name in boss_names.BOSS_NAMES:
        await embed_generator.post_boss_embed(ctx, data, name, number_of_placements=3)


@bot.tree.command()
async def submit(
    interaction: discord.Interaction,
    username: str,
    pb: str,
    bossname: BossName,
    group_size: int,
    image: discord.Attachment,
):
    # Check if the user uploaded an image
    if image is None:
        await interaction.response.send_message("Please upload an image.")
        return

    # Print the submitted information for testing
    await interaction.response.send_message(
        f"{username} is submitting a \nPB: {pb} for \: {bossname}\n Please wait for admin approval\n{image.url}",
    )

    # todo emoji reacts and approval channels


bot.run(bot_token)
