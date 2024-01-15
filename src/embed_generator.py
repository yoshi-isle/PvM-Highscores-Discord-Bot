from discord import Embed
import constants.osrs_wiki as wiki
import helpers.embed_content_builder
import helpers.data_helper
import time


async def post_boss_embed(ctx, data, boss_name, number_of_placements):
    """
    Builds an embed for boss times
    """
    data = helpers.data_helper.get_fastest_times(data, boss_name)

    embed = Embed(title=boss_name)

    embed.set_thumbnail(url=wiki.CDN_URLS[boss_name])
    embed_content = helpers.embed_content_builder.build_boss_embed_content(
        data, number_of_placements
    )
    embed.add_field(name="", value=embed_content, inline=False)

    # We don't want to rate limit ourselves. Embeds must be posted slowly
    time.sleep(6)
    await ctx.send(embed=embed)


async def post_raids_embed(ctx, data, raid_name, pb_categories, number_of_placements):
    """
    Builds an embed for raids. Slightly different than bosses because it uses multiple fields
    """
    data = helpers.data_helper.get_fastest_times(data, raid_name)
    embed = Embed(title=raid_name)
    embed.set_thumbnail(url=wiki.CDN_URLS[raid_name])

    # Iterate through & generate the pb categories we want to show
    for category in pb_categories:
        embed_content = helpers.embed_content_builder.build_raid_embed_content(
            data, number_of_placements, category
        )
        if embed_content == "":
            embed_content = "*(Needs submission)*"
        embed.add_field(
            name=category_names[category], value=embed_content, inline=False
        )

    # We don't want to rate limit ourselves. Embeds must be posted slowly
    print("Updating embed for " + raid_name)
    time.sleep(5)
    await ctx.send(embed=embed)


category_names = {
    1: "Solo",
    2: "Duo",
    3: "Trio",
    4: "4-man",
    5: "5-man",
}
