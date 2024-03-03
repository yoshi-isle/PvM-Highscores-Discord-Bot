from datetime import datetime

import discord
from discord import Embed

import hall_of_fame.data_helper as data_helper
import hall_of_fame.embed_content_builder as embed_content_builder


async def generate_pb_embed(data, boss_info, number_of_placements):
    """
    Builds an embed for boss times
    """
    boss_name = boss_info["boss_name"]
    data = data_helper.get_fastest_times(data, boss_name)

    embed = Embed(title=f"__{boss_name}__")

    embed.set_thumbnail(url=boss_info["thumbnail"])
    embed_content = await embed_content_builder.build_embed_content(data, number_of_placements)
    embed.add_field(name="", value=embed_content, inline=False)

    return embed


async def generate_pb_submission_embed(title: str, description: str, color, timestamp, image_url, footer_id):
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
