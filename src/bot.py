import copy
from datetime import datetime
import json
import typing

import discord
from discord import app_commands
from discord.ext import commands

import constants.boss_names as boss_names
import constants.raid_names as raid_info

from database import Database
import embed_generator
from constants.colors import Colors
from dartboard import Dartboard
from helpers.time_helpers import validate_time_format, convert_pb_to_time

import data.personal_best as personal_best
import uuid

# Import keys
with open("../config/appsettings.local.json") as appsettings:
    data = json.load(appsettings)

bot_token = data["BotToken"]
channel_id = data["HighscoresChannelId"]


bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

dartboard = Dartboard()

PENDING = "Pending "
APPROVED = "Approved "
FAILED = "Failed "
PB_SUBMISSION = "PB Submission"


@bot.event
async def on_ready():
    await bot.tree.sync()


@bot.command()
async def raidpbs(ctx):
    channel = ctx.channel
    await channel.purge()
    database = Database()
    data = database.get_personal_bests()

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
    database = Database()
    data = database.get_personal_bests()

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


class PbTimeConverter(app_commands.Transformer):
    async def transform(self, interaction: discord.Interaction, value: str):
        case = await validate_time_format(value)
        if case:
            return await convert_pb_to_time(case, value)

        raise discord.app_commands.TransformerError(value=value)


@bot.tree.command(name="submit_boss_pb")
@app_commands.describe(boss_name="Submit a boss PB")
@app_commands.autocomplete(boss_name=submit_boss_pb_autocomplete)
async def submit_boss_pb(
    interaction: discord.Interaction,
    pb: PbTimeConverter,
    boss_name: str,
    osrs_username: str,
    image: discord.Attachment,
):
    approve_channel = bot.get_channel(data["ApproveChannelId"])

    if image is None:
        await interaction.response.send_message("Please upload an image.")
        return

    # Todo: check if boss is equal to one in the submit_boss_pb_autocomplete list (spelled correctly. case-sensitive)

    description = f"@{interaction.user.display_name} is submitting a PB of: {pb} for **{boss_name}**!\n\nClick the '👍' to approve."

    time_of_submission = datetime.now()

    # Build the PersonalBest model and insert a record
    pb = personal_best.PersonalBest(
        id=uuid.uuid4(),
        boss=boss_name,
        pb=pb,
        approved=False,
        date_achieved=time_of_submission,
        discord_cdn_url=image.url,
        osrs_username=osrs_username,
        discord_username=interaction.user.display_name,
    )

    database = Database()
    _id = database.insert_personal_best_submission(pb)

    embed = await embed_generator.generate_pb_submission_embed(
        title=PENDING + PB_SUBMISSION,
        description=description,
        color=Colors.yellow,
        timestamp=time_of_submission,
        image_url=image.url,
        footer_id=_id,
    )

    message = await approve_channel.send(embed=embed)
    await message.add_reaction("👍")
    await message.add_reaction("👎")

    await interaction.response.send_message("Submission is pending!", ephemeral=True)


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


@bot.tree.error
async def on_app_command_error(interaction: discord.Interaction, error):
    if isinstance(error, discord.app_commands.TransformerError):
        error_message = f"The following time of **{error.value}** did not conform to the time format. It needs to be in 00:00.00 format"
        await interaction.response.send_message(f"{error_message}", ephemeral=True)


@bot.event
async def on_raw_reaction_add(payload):
    """
    This is a check for every reaction that happens
    """
    # ignore the reactions from the bot
    member = payload.member
    if member.bot:
        return

    # only check the reactions on the approve channel
    channel = bot.get_channel(payload.channel_id)
    if channel.id == data["ApproveChannelId"]:
        # grab the actual message the reaction was too
        message = await channel.fetch_message(payload.message_id)

        # the message must contain an embed
        if message.embeds:
            embed = message.embeds[0]

            # We only want to edit pending submissions
            if "Pending" in embed.title:
                new_prefix = ""
                new_color = ""

                # approved submission
                if payload.emoji.name == "👍":
                    await channel.send("Submission approved! 👍", reference=message)
                    new_prefix = APPROVED
                    new_color = Colors.green
                # not approved submission
                elif payload.emoji.name == "👎":
                    await channel.send("Submission not approved 👎", reference=message)
                    new_prefix = FAILED
                    new_color = Colors.red

                # deep copy so that we can update the embed
                new_embed = copy.deepcopy(embed)
                new_embed.title = new_prefix + PB_SUBMISSION
                new_embed.color = new_color

                # todo: this is where we'll update approval to true
                database = Database()
                record = database.get_personal_best_by_id(embed.footer.text)

                await message.edit(embed=new_embed)
                await message.clear_reactions()


bot.run(bot_token)
