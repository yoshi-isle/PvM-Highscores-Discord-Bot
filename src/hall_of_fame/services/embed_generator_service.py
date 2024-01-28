from asyncio import sleep

from discord import Embed

import constants.osrs_wiki as wiki
import hall_of_fame.data_helper as dh
from hall_of_fame.time_helpers import convert_pb_to_display_format

import datetime

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
    embed_content = await build_embed_content(data, number_of_placements)
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


async def build_embed_content(data, number_of_placements):
    """
    Builds formatted embed content from player data for pbs, showing top placements. Assumes data is sorted
    """
    embed_content = ""
    current_placement = 1

    for i in range(len(data)):
        pb = await convert_pb_to_display_format(
            datetime.time.fromisoformat(data[i]["pb"])
        )
        emoji = PLACEMENT_EMOJI[current_placement]
        username = data[i]["osrs_username"]

        if current_placement > number_of_placements:
            return embed_content
        embed_content += f"{emoji} {username} - {pb}\n"
        if i != len(data) - 1:
            # If the next pb is slower, we can increase the placement for the next insert
            if data[i + 1]["pb"] > data[i]["pb"]:
                current_placement = current_placement + 1

    return embed_content


PLACEMENT_EMOJI = {
    1: ":first_place:",
    2: ":second_place:",
    3: ":third_place:",
    4: "",
    5: "",
}
