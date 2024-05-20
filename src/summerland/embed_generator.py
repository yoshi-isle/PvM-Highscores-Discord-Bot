import discord
from discord import Embed
from constants.colors import Colors


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
