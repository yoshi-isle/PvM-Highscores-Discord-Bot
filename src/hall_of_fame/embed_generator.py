from asyncio import sleep

from discord import Embed

import constants.osrs_wiki as wiki
import hall_of_fame.data_helper as dh
import hall_of_fame.embed_content_builder as ecb
from constants.colors import Colors
from hall_of_fame.constants.personal_best import PersonalBest

CATERGORY_NAMES = {
    1: "Solo",
    2: "Duo",
    3: "Trio",
    4: "4-man",
    5: "5-man",
}


async def post_boss_embed(ctx, data, boss_name, number_of_placements):
    """
    Builds an embed for boss times
    """
    data = dh.get_fastest_times(data, boss_name)

    embed = Embed(title=boss_name, color=Colors.light_purple)

    embed.set_thumbnail(url=wiki.CDN_URLS[boss_name])
    embed_content = ecb.build_embed_content(data, number_of_placements)
    embed.add_field(name="", value=embed_content, inline=False)

    # We don't want to rate limit ourselves. Embeds must be posted slowly
    sleep(1)
    await ctx.send(embed=embed)


async def post_raids_embed(ctx, data, raid_name, pb_categories, number_of_placements):
    """
    Builds an embed for raids. Slightly different than bosses because it uses multiple fields
    """
    data = dh.get_fastest_times(data, raid_name)

    embed = Embed(title=raid_name)
    embed.set_thumbnail(url=wiki.CDN_URLS[raid_name])

    # Iterate through & generate the pb categories we want to show
    for category in pb_categories:
        filtered_data = list(
            result for result in data if result["groupSize"] == category
        )

        embed_content = ecb.build_embed_content(filtered_data, number_of_placements)
        if embed_content == "":
            embed_content = "None"
        embed.add_field(
            name=CATERGORY_NAMES[category], value=embed_content, inline=False
        )

    print("Updating embed for " + raid_name)

    # We don't want to rate limit ourselves. Embeds must be posted slowly
    sleep(1)
    await ctx.send(embed=embed)


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