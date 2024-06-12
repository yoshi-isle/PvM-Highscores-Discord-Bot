import discord
import datetime
from discord import Embed
from constants.colors import Colors
from summerland.constants.tiles import BINGO_TILES
from summerland.constants.team_icon_emojis import TEAM_ICON_EMOJIS
from datetime import datetime, timedelta
import time
from art import text2art


async def draw_dice_result(roll):
    linesep = "\n"
    embed = Embed()
    top_border = "━━━━━━━━━━━━━━━━━▼━━━━━━━━━━━━━━━━━"
    side_border = "|"
    # get the ascii art, split on new lines to then apply the centering
    raw_art = text2art(str(roll), font="fraktur").split("\n")
    # remove the last 3 lines ':-3' because they are just blank
    formatted_art = linesep.join(
        side_border + line.center(33) + side_border for line in raw_art[:-3]
    )
    embed.add_field(
        name="Rolling...",
        value=f"```{top_border}\n{formatted_art}\n{top_border}```",
        inline=False,
    )
    return embed


async def generate_final_results():
    embed = discord.Embed(
        title="__**Final Results**__",
        description=":1stplacecrown: <:orca:1245396728094654485> Orca Team\n:2ndplacecrown: <:octopus:1245396876426215574> Squidrific\n\nWhalers <:whale:1246256962815918183> - Tile 100: 5x Echo Crystals OR 1x Ralos (MUST BE COMPLETED)\nThe Busty Crustaceans <:crab:1245396597345615983> - Tile 96: Any 3x Lightbearers or Fangs\nNemo <:clownfish:1245396742065881241> - Tile 91: 5x Armor Seeds OR Enhanced Weapon Seed\nRays <:stingray:1246257550559547442> - Tile 88: Any Zalcano unique\nOnlyPhins <:dolphin:1245396627213258833> - Tile 80: Feather Hunter CA\nSea Turtle <:sea_turtle:1245396703977406605> - Tile 58: Any NM unique (not Slepey Tablet)",
        colour=Colors.green,
    )
    embed.set_thumbnail(url=trailblazer_trophy_image_url)
    embed.set_footer(
        text="discord.gg/kittycats", icon_url="https://i.imgur.com/RT1AlJj.png"
    )

    return embed


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


async def generate_team_embed(team, current_placement):
    """
    Builds the embed message string that will get posted to the channel
    """
    embed = Embed(
        title=f"__**{team['team_name']}** Information__",
        colour=Colors.light_purple,
    )

    # Cool looking discord timestamp
    twelve_hours_from_now = team["last_reroll"] + timedelta(hours=12)
    epoch = round(twelve_hours_from_now.timestamp())
    disc_dt = f"<t:{epoch}:R>"

    embed.add_field(
        name=f"🔷 Members",
        value=f"{await generate_team_members_list(team['team_members'])}",
        inline=True,
    )
    embed.add_field(
        name="🔲 Current Tile",
        value=f"{await generate_tile_information(team)}\n{await can_we_reroll(team, disc_dt)}\n≫─────────────≪\n> Current Rank: {current_placement}\n> https://discord.com/channels/847313025919746129/1245222266225168424",
        inline=True,
    )

    embed.set_thumbnail(url=team["team_image"])
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
        value=f"[Wiki URL]({BINGO_TILES[team['current_tile']]['WikiUrl']})\n*Check out your ranking here* https://discord.com/channels/847313025919746129/1245222266225168424",
        inline=False,
    )

    embed.add_field(
        name="",
        value=f"Your re-roll timer has reset to {disc_dt}",
        inline=False,
    )

    if BINGO_TILES[team["current_tile"]]["Challenge"] != "":
        embed.add_field(
            name="",
            value=f"Your tile has a challenge tile! @Tangy or @Kanao if you finish it and the player(s) who contributed to it will win bonds!\n**{BINGO_TILES[team['current_tile']]['Challenge']}**",
            inline=False,
        )

    embed.set_thumbnail(url=team["team_image"])
    embed.set_image(url=BINGO_TILES[team["current_tile"]]["Image"])
    embed.set_footer(
        text="discord.gg/kittycats", icon_url="https://i.imgur.com/RT1AlJj.png"
    )

    return embed


async def generate_setback_or_skip_embed(new_tile, title, value):
    """
    Builds the embed message string that will get posted to the channel
    """
    tile = BINGO_TILES[new_tile]
    embed = Embed(
        title=title,
    )

    embed.add_field(
        name="",
        value=value,
        inline=False,
    )

    embed.set_image(url=tile["Image"])
    embed.set_footer(
        text="discord.gg/kittycats", icon_url="https://i.imgur.com/RT1AlJj.png"
    )

    return embed


async def generate_changelog_setback_or_skip_embed(going_forward, team_info, new_tile):
    """
    Builds the embed message string that will get posted to the channel
    """
    tile = BINGO_TILES[new_tile]
    embed = Embed(
        title="",
    )
    if going_forward:
        embed.title = f"{team_info['team_name']} skips-forward!"
        embed.color = Colors.green
    else:
        embed.title = f"{team_info['team_name']} has been set-back..."
        embed.color = Colors.red

    embed.add_field(
        name="",
        value=BINGO_TILES[new_tile]["Name"],
        inline=False,
    )

    embed.set_thumbnail(url=team_info["team_image"])
    embed.set_image(url=tile["Image"])
    embed.set_footer(
        text="discord.gg/kittycats", icon_url="https://i.imgur.com/RT1AlJj.png"
    )

    return embed


async def generate_rerolled_tile_embed(team):
    """
    Builds the embed message string that will get posted to the channel
    """
    embed = Embed(
        title=f"__**Your Rerolled Tile:**__",
    )

    # Cool looking discord timestamp
    epoch = round(team["last_reroll"].timestamp())
    disc_dt = f"<t:{epoch}:R>"

    embed.add_field(
        name=f"{BINGO_TILES[team['current_tile']]['Name']}",
        value=f"\n*Check out your ranking here* https://discord.com/channels/847313025919746129/1245222266225168424",
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
        value=f"✅ - **Approve** the tile OR partial credit\n❌ - **Deny** (please tell them why)\n🎲 - **FORCE** roll (in case of an alternate completion)",
        inline=False,
    )

    embed.set_image(url=image)
    embed.set_footer(text=uuid)

    return embed


async def update_admin_approved_embed(embed):
    """
    Updates the admin approved embed message
    """

    new_embed = embed
    new_embed.title = "[APPROVED]"
    new_embed.color = Colors.green
    new_embed.remove_footer()
    return new_embed


async def update_admin_denied_embed(embed):
    """
    Updates the admin approved embed message
    """

    new_embed = embed
    new_embed.title = "[DENIED]"
    new_embed.color = Colors.red
    new_embed.remove_footer()
    return new_embed


async def update_channel_approved_embed(embed):
    """
    Updates the admin approved embed message
    """
    new_embed = embed
    new_embed.color = Colors.green
    new_embed.title = "[Approved]"
    new_embed.remove_field(1)
    new_embed.remove_footer()
    return new_embed


async def update_denied_approved_embed(embed):
    """
    Updates the admin approved embed message
    """
    new_embed = embed
    new_embed.color = Colors.red
    new_embed.title = "[Denied]"
    new_embed.remove_field(1)
    new_embed.remove_footer()
    return new_embed


async def generate_dice_roll_embed(roll):
    """
    Builds the embed message string that will get posted to the channel
    """
    embed = Embed(title="🎲 Rolling...", description=f"Your team rolled a **{roll}**")

    return embed


async def generate_team_members_list(members):
    team_members_list = ""
    for member in members:
        team_members_list += f"> {member}\n"
    return team_members_list


async def generate_tile_information(team):
    tile_information = (
        f"> **{BINGO_TILES[team['current_tile']]['Name']} (#{team['current_tile']})**"
    )
    if BINGO_TILES[team["current_tile"]]["CompletionCounter"] > 1:
        tile_information += f"\n> Completed **{team['progress_counter']}** out of **{BINGO_TILES[team['current_tile']]['CompletionCounter']}**"
    return tile_information


async def can_we_reroll(team, disc_dt):
    twelve_hours_from_now = team["last_reroll"] + timedelta(hours=12)
    if datetime.now() > twelve_hours_from_now:
        return "> **🎲 Your team is eligible for a re-roll!**"
    return f"> Time until re-roll: {disc_dt}"
