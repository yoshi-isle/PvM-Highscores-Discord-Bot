import discord
import datetime
from discord import Embed
from constants.colors import Colors
from summerland.constants.tiles import BINGO_TILES


async def generate_top_teams_embed(current_standings_text):
    """
    Builds the embed message string that will get posted to the channel
    """
    trailblazer_trophy_image_url = "https://oldschool.runescape.wiki/images/Trailblazer_reloaded_dragon_trophy.png?4f4fe"
    embed = Embed(
        title="__**Top Teams:**__",
        colour=Colors.light_blue,
    )

    embed.add_field(name="", value=current_standings_text, inline=False)
    embed.set_thumbnail(url=trailblazer_trophy_image_url)
    embed.set_footer(
        text="discord.gg/kittycats", icon_url="https://i.imgur.com/RT1AlJj.png"
    )

    return embed


async def generate_team_embed(team):
    """
    Builds the embed message string that will get posted to the channel
    """
    embed = Embed(
        title=f"__**{team['team_name']}**__",
        colour=Colors.light_purple,
    )

    # Cool looking discord timestamp
    epoch = round(team["last_reroll"].timestamp())
    disc_dt = f"<t:{epoch}:R>"

    embed.add_field(
        name="🔹 Team Information",
        value=f"> Team Number: {team['team_number']}\n> Time until re-roll: {disc_dt}\n",
        inline=False,
    )
    embed.add_field(
        name="🔸 Members",
        value=f"{await generate_team_members_list(team['team_members'])}",
        inline=False,
    )
    embed.add_field(
        name="🔲 Current Tile",
        value=f"{await generate_tile_information(team)}\n\n*Check out your ranking here* https://discord.com/channels/1197595466657968158/1237804690570481715",
        inline=False,
    )

    embed.set_image(url=BINGO_TILES[team["current_tile"]]["Image"])
    embed.set_footer(
        text="discord.gg/kittycats", icon_url="https://i.imgur.com/RT1AlJj.png"
    )

    return embed


async def generate_new_tile_embed(team):
    """
    Builds the embed message string that will get posted to the channel
    """
    embed = Embed(
        title=f"__**Your New Tile:**__",
    )

    # Cool looking discord timestamp
    epoch = round(team["last_reroll"].timestamp())
    disc_dt = f"<t:{epoch}:R>"

    embed.add_field(
        name=f"{BINGO_TILES[team['current_tile']]['Name']}",
        value=f"\n*Check out your ranking here* https://discord.com/channels/1197595466657968158/1237804690570481715",
        inline=False,
    )

    embed.add_field(
        name="",
        value=f"Your re-roll timer has reset to {disc_dt}",
        inline=False,
    )

    embed.set_image(url=BINGO_TILES[team["current_tile"]]["Image"])
    embed.set_footer(
        text="discord.gg/kittycats", icon_url="https://i.imgur.com/RT1AlJj.png"
    )

    return embed


async def generate_submission_receipt_embed(uuid, image, interaction, tile):
    """
    Builds the embed message string that will get posted to the channel
    """
    embed = Embed(
        title=f"__**We've Received Your Submission!**__",
        colour=Colors.yellow,
    )

    embed.add_field(
        name="🟡 Information",
        value=f"> **Submitted by:** {interaction.user.display_name}\n> **Tile:** {tile['Name']}\n",
        inline=False,
    )

    embed.add_field(
        name="Please wait",
        value=f"Once a bingo admin approves your tile, your progress will be automatically updated.",
        inline=False,
    )

    embed.set_image(url=image)
    embed.set_footer(text=uuid)

    return embed


async def generate_admin_approval_embed(
    uuid, image, interaction, team_info, tile, is_partial
):
    """
    Builds the embed message string that will get posted to the channel
    """

    embed = Embed(
        title=f"__**Pending Submission**__",
        colour=Colors.yellow,
    )

    embed.add_field(
        name="🟡 __Information__",
        value=f"> **Team: **{team_info['team_name']}\n> **Team Channel:**{interaction.channel.mention}\n> **Submitted by:** {interaction.user.display_name}\n> **Tile:** {tile['Name']}\n",
        inline=False,
    )

    if is_partial:
        embed.add_field(
            name="🟣 __This is a PARTIAL submission__",
            value=f"> **Current Progress:** {team_info['progress_counter']} out of {tile['CompletionCounter']}",
            inline=False,
        )

    embed.add_field(
        name="__Admin Options__",
        value=f"👍 - **Approve** the tile OR partial credit\n👎 - **Deny** (please tell them why)\n🎲 - **FORCE** roll (in case of an alternate completion)",
        inline=False,
    )

    embed.set_image(url=image)
    embed.set_footer(text=uuid)

    return embed


async def generate_dice_roll_embed(roll):
    """
    Builds the embed message string that will get posted to the channel
    """
    embed = Embed(
        title=f"__**Dice Roll...**__",
        colour=Colors.green,
    )

    embed.add_field(
        name="",
        value=f"Your team rolled a **{roll}**",
        inline=False,
    )

    embed.set_image(url="https://i.imgflip.com/6clv39.gif")
    embed.set_footer(
        text="discord.gg/kittycats", icon_url="https://i.imgur.com/RT1AlJj.png"
    )
    return embed


async def generate_team_members_list(members):
    team_members_list = ""
    for member in members:
        team_members_list += f"> {member}\n"
    return team_members_list


async def generate_tile_information(team):
    tile_information = f"> **Your team is on tile #{team['current_tile']}**: {BINGO_TILES[team['current_tile']]['Name']}"
    if BINGO_TILES[team["current_tile"]]["CompletionCounter"] > 1:
        tile_information += f"\n> Completed **{team['progress_counter']}** out of **{BINGO_TILES[team['current_tile']]['CompletionCounter']}**"
    return tile_information
