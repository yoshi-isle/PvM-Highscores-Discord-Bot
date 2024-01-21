import discord
import json
import typing
import embed_generator
import database
import constants.boss_names as boss_names
import constants.raid_names as raid_info
from discord.ext import commands
from discord import Interaction, SelectOption, ButtonStyle
from enum import Enum
import typing
import datetime
from discord import app_commands
from dartboard import Dartboard
import asyncio
import copy

# Import keys
with open("../config/appsettings.local.json") as appsettings:
    data = json.load(appsettings)

bot_token = data["BotToken"]
channel_id = data["HighscoresChannelId"]


bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

dartboard = Dartboard()
YELLOW = 0xF5ED00
GREEN = 0x006400
RED = 0x800000
PENDING = "Pending "
APPROVED =  "Approved "
FAILED =  "Failed "
PB_SUBMISSION="PB Submission"


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
    for boss_name in boss_names.BOSS_NAMES:
        if current.lower() in boss_name.lower():
            data.append(app_commands.Choice(name=boss_name, value=boss_name))
    return data


@bot.tree.command(name="submit_boss_pb")
@app_commands.describe(boss_name="Submit a boss PB")
@app_commands.autocomplete(boss_name=submit_boss_pb_autocomplete)
async def submit_boss_pb(
    interaction: discord.Interaction,
    pb: str,
    boss_name: str,
    image: discord.Attachment,
):
    approveChannel = bot.get_channel(data["ApproveChannel"])
    
    if image is None:
        await interaction.response.send_message("Please upload an image.")
        return

    # Todo: check PB to be MM:ss:mm format
    # Todo: check if boss is equal to one in the submit_boss_pb_autocomplete list (spelled correctly. case-sensitive)
    

    description=f"@{interaction.user.display_name} is submitting a PB of: {pb} for **{boss_name}**!\n\nClick the '👍' to approve."

    time_of_submission = datetime.datetime.now()

    embed = await embed_generator.generate_pb_submission_embed(title=PENDING+PB_SUBMISSION, description=description, color=YELLOW, timestamp=time_of_submission,image_url=image.url)

    await approveChannel.send(embed=embed)


async def throw_a_dart_autocomplete(
    interaction: discord.Interaction,
    current: str,
) -> typing.List[app_commands.Choice[str]]:
    data = []
    for team_name in [
        "Sapphire",
        "Ruby",
        "Emerald",
        "Diamond",
        "Dragonstone",
        "Opal",
        "Jade",
        "Topaz",
    ]:
        if current.lower() in team_name.lower():
            data.append(app_commands.Choice(name=team_name, value=team_name))
    return data


@bot.tree.command(name="throw_a_dart")
@app_commands.describe(team="Generate a new task for your team")
@app_commands.autocomplete(team=throw_a_dart_autocomplete)
async def throw_a_dart(
    interaction: discord.Interaction,
    team: str,
):
    new_task = dartboard.get_task()
    embed = await embed_generator.generate_dartboard_task_embed(
        team_name=f"{team}",
        task=new_task,
    )

    await interaction.response.send_message(embed=embed)


@bot.event
async def on_raw_reaction_add(payload):
    channel = bot.get_channel(payload.channel_id)
    await channel.send("level0")
    if channel.id == bot.get_channel(data["ApproveChannel"]):
        await channel.send("level1")
        message = await channel.fetch_message(payload.message_id)
        embed =  message.embeds[0]
        new_embed = copy.deepcopy(embed)
        await channel.send(f"{embed.title}")
        if "Pending" in embed.title:
            await channel.send("level2")
            if payload.emoji.name == "👍":
                await channel.send('Submission approved! 👍', reference=message)
                new_prefix = APPROVED
                new_color = GREEN
            elif payload.emoji.name == "👎":
                await channel.send('Submission not approved 👎', reference=message)
                new_prefix = FAILED
                new_color = RED
            new_embed.title = new_prefix+PB_SUBMISSION
            new_embed.color = new_color
            await message.edit(embed=new_embed)
            await message.clear_reactions()


bot.run(bot_token)
