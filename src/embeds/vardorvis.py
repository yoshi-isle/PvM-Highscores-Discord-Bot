from discord import Embed
import helpers.osrswiki
import helpers.embed_content_builder
import helpers.data_helper

boss_name = "Vardorvis"

async def post_embed(ctx, data):
    data = helpers.data_helper.get_fastest_times(data, boss_name)

    embed = Embed(title=boss_name, color=0xFF1E6D)

    embed.set_thumbnail(url=helpers.osrswiki.vardorvis_url)
    embed_content = helpers.embed_content_builder.build(data, 3)
    embed.add_field(name="", value=embed_content, inline=False)

    await ctx.send(embed=embed)