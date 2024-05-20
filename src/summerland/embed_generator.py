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
    embed.set_footer(text="discord.gg/kittycats")

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
    epoch = round(team['last_reroll'].timestamp())
    disc_dt = f"<t:{epoch}:R>"

    embed.add_field(name="🔹 Team Information", value=f"> Team Number: {team['team_number']}\n> Time until re-roll: {disc_dt}\n", inline=False)
    embed.add_field(name="🔸 Members", value=f"{await generate_team_members_list(team['team_members'])}", inline=False)
    embed.add_field(name="🔲 Current Tile", value=f"{await generate_tile_information(team)}\n\n*Check out your ranking here* https://discord.com/channels/1197595466657968158/1237804690570481715", inline=False)
    
    embed.set_image(url=BINGO_TILES[team['current_tile']]['Image'])
    embed.set_footer(text="discord.gg/kittycats")

    return embed

async def generate_team_members_list(members):
    team_members_list = ""
    for member in members:
        team_members_list += f"> {member}\n"
    return team_members_list

async def generate_tile_information(team):
    tile_information = f"> **Your team is on tile #{team['current_tile']}**: {BINGO_TILES[team['current_tile']]['Name']}"
    if (BINGO_TILES[team['current_tile']]['CompletionCounter'] > 1):
        tile_information += f"> Completed **{team['progress_counter']}** out of **{BINGO_TILES[team['current_tile']]['CompletionCounter']}**"
    return tile_information