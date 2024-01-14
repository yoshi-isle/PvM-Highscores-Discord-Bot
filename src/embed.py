from discord import Embed
import helpers.osrswiki
import helpers.embed_content_builder
import helpers.data_helper

async def post_boss_embed(ctx, data, boss_name):
    data = helpers.data_helper.get_fastest_times(data, boss_name)

    embed = Embed(title=boss_name)

    embed.set_thumbnail(url=helpers.osrswiki.CDN_URLS[boss_name])
    embed_content = helpers.embed_content_builder.build_embed_content(data, 3)
    embed.add_field(name="", value=embed_content, inline=False)

    await ctx.send(embed=embed)

async def post_raids_embed(ctx, data, raid_name):
    data = helpers.data_helper.get_fastest_raid_times(data, raid_name)

    embed = Embed(title=raid_name)

    embed.set_thumbnail(url=helpers.osrswiki.CDN_URLS[raid_name])
    embed_content = helpers.embed_content_builder.build_embed_content(data, 3)
    embed.add_field(name="", value=embed_content, inline=False)

    await ctx.send(embed=embed)