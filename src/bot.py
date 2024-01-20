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
from discord import app_commands
import typing
import datetime

# Import keys
with open("../config/appsettings.local.json") as appsettings:
    data = json.load(appsettings)

bot_token = data["BotToken"]
channel_id = data["HighscoresChannelId"]

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())


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


async def submit_boss_pb_autocomplete(
    interaction: discord.Interaction,
    current: str,
) -> typing.List[app_commands.Choice[str]]:
    data = []
    for boss_name in [
        "Nightmare (Solo)",
        "Phosani's Nightmare",
        "Vardorvis",
        "Duke Succellus",
        "The Whisperer",
        "Leviathan",
        "Vardorvis (Awakened)",
        "Duke Succellus (Awakened)",
        "The_Whisperer (Awakened)",
        "Leviathan (Awakened)",
        "Inferno",
        "Fight Caves",
        "The Gauntlet",
        "The Corrupted Gauntlet",
        "Zulrah",
        "Vorkath",
        "Grotesque Guardians",
        "Alchemical Hydra",
        "Phantom Muspah",
        "Hespori",
        "Mimic",
        "Hallowed Sepulchre",
    ]:
        if current.lower() in boss_name.lower():
            data.append(app_commands.Choice(name=boss_name, value=boss_name))
    return data


@bot.tree.command(name="submit_boss_pb")
@app_commands.describe(boss_name="Submit a boss PB")
@app_commands.autocomplete(boss_name=submit_boss_pb_autocomplete)
async def submit_boss_pb(
    interaction: discord.Interaction,
    username: str,
    pb: str,
    boss_name: str,
    image: discord.Attachment,
):
    if image is None:
        await interaction.response.send_message("Please upload an image.")
        return

    # Todo: check PB to be MM:ss:mm format
    embed = discord.Embed(
        title="PB Submission",
        description=f"**{username}** is submitting a PB of: {pb} for **{boss_name}**!",
        colour=0xF5ED00,
        timestamp=datetime.datetime.now(),
    )

    embed.set_image(url=image.url)

    embed.set_footer(
        icon_url="https://oldschool.runescape.wiki/images/Trailblazer_reloaded_dragon_trophy.png?4f4fe"
    )


    message = await interaction.channel.send(embed=embed)
    await message.add_reaction('👍')


bot.run(bot_token)
