from discord import Embed

import constants.osrs_wiki as wiki
import hall_of_fame.data_helper as dh
import hall_of_fame.embed_content_builder as ecb

CATERGORY_NAMES = {
    1: "Solo",
    2: "Duo",
    3: "Trio",
    4: "4-man",
    5: "5-man",
}


async def generate_pb_embed(data, boss_name, number_of_placements):
    """
    Builds an embed for boss times
    """
    data = dh.get_fastest_times(data, boss_name)

    embed = Embed(title=boss_name)

    embed.set_thumbnail(url=wiki.CDN_URLS[boss_name])
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
