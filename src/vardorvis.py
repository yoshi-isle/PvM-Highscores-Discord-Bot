from discord import Embed
import osrswiki

async def Update(ctx):
    embed = Embed(title="Vardorvis", color=0xFF1E6D)
    embed.add_field(
        name="",
        value=":first_place:  Kitty Neko - 0:36\n :second_place:  Yoshe - 0:48\n :third_place:  Xavierman73 - 2:56",
        inline=False
    )

    embed.set_thumbnail(url=osrswiki.vardorvisCdnUrl)
    await ctx.send(embed=embed)