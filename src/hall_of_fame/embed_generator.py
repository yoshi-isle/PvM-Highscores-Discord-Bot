from discord import Embed
import discord

import hall_of_fame.data_helper as dh
import hall_of_fame.embed_content_builder as ecb

from datetime import datetime

CATERGORY_NAMES = {
    1: "Solo",
    2: "Duo",
    3: "Trio",
    4: "4-man",
    5: "5-man",
}


async def generate_pb_embed(data, boss_info, number_of_placements):
    """
    Builds an embed for boss times
    """
    data = dh.get_fastest_times(data, boss_info["boss_name"])

    embed = Embed(title=boss_info["boss_name"])

    embed.set_thumbnail(url=boss_info["thumbnail"])
    embed_content = await ecb.build_embed_content(data, number_of_placements)
    embed.add_field(name="", value=embed_content, inline=False)

    return embed


async def generate_pb_submission_embed(
    title: str, description: str, color, timestamp, image_url, footer_id
):
    """
    Builds the embed message string that will get posted to the channel
    """
    trailblazer_trophy_image_url = "https://oldschool.runescape.wiki/images/Trailblazer_reloaded_dragon_trophy.png?4f4fe"
    embed = Embed(
        title=title,
        description=description,
        colour=color,
        timestamp=timestamp,
    )

    embed.set_image(url=image_url)
    embed.set_footer(text=footer_id, icon_url=trailblazer_trophy_image_url)

    return embed


async def generate_how_to_submit_embed():
    embed = discord.Embed(colour=0xFFFFFF, timestamp=datetime.now())

    embed.set_author(name="How do I submit?")

    embed.add_field(
        name="Submitting a PB (Personal Best)",
        value="Some instructions here about submitting a PB. Some instructions here about submitting a PB. Some instructions here about submitting a PB. Some instructions here about submitting a PB. Some instructions here about submitting a PB.",
        inline=False,
    )
    embed.add_field(
        name="Submitting a KC (Kill Count)",
        value="Some instructions here about submitting a KC. Some instructions here about submitting a KC. Some instructions here about submitting a KC. Some instructions here about submitting a KC.",
        inline=False,
    )

    embed.set_thumbnail(
        url="https://oldschool.runescape.wiki/images/thumb/Cake_of_guidance_detail.png/130px-Cake_of_guidance_detail.png?c3595"
    )

    embed.set_footer(text="Kitty Meowseum")

    return embed
