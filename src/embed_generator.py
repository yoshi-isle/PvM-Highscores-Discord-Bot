from discord import Embed
from dartboard import Task
import constants.osrs_wiki as wiki
import helpers.embed_content_builder as ecb
import helpers.data_helper as dh
import time
import datetime

LIGHT_BLUE = 0x00b0f4

async def post_boss_embed(ctx, data, boss_name, number_of_placements):
    """
    Builds an embed for boss times
    """
    data = dh.get_fastest_times(data, boss_name)

    embed = Embed(title=boss_name)

    embed.set_thumbnail(url=wiki.CDN_URLS[boss_name])
    embed_content = ecb.build_embed_content(data, number_of_placements)
    embed.add_field(name="", value=embed_content, inline=False)

    # We don't want to rate limit ourselves. Embeds must be posted slowly
    time.sleep(1)
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
            name=category_names[category], value=embed_content, inline=False
        )

    print("Updating embed for " + raid_name)

    # We don't want to rate limit ourselves. Embeds must be posted slowly
    time.sleep(1)
    await ctx.send(embed=embed)


category_names = {
    1: "Solo",
    2: "Duo",
    3: "Trio",
    4: "4-man",
    5: "5-man",
}


async def generate_dartboard_task_embed(team_name:str, task: Task):
    """
    Builds the embed message string that will get posted to the channel
    """

    embed = Embed(title=f"The {team_name} team must get {task.task_name}!",
                            description=f"{task.task_description}",
                            colour=LIGHT_BLUE,
                            timestamp=datetime.datetime.now())

    embed.set_author(name="Kitty Bot")

    embed.add_field(name=f"Dice roll result:",
                    value=f"{task.task_number}",
                    inline=True)
    embed.add_field(name=f"Point value",
                    value=f"{task.task_points}",
                    inline=True)
    
    if task.task_challenge_name:
            # this blank field is for spacing purposes
            embed.add_field(name="",
                            value="",
                            inline=False)
            embed.add_field(name=f"Complete this challenge and win the bonus challenge points!",
                    value=f"{task.task_challenge_description}",
                    inline=True)
            embed.add_field(name="Challenge points",
                    value=f"{task.task_challenge_points}",
                    inline=True)

    embed.set_thumbnail(url=task.image_link)

    embed.set_footer(text="👞🗑️")

    return embed