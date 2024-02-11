import logging
from typing import Literal, Optional

import discord
from discord import app_commands
from discord.ext import commands
from management.random_emoji import (
    get_random_achievement_emoji,
    get_random_drop_emoji,
    get_random_floof_emoji,
)
from management.random_greeting import get_random_greeting_url

from constants.channels import ChannelIds
from math import ceil


class StaticEmbed(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.logger = logging.getLogger("discord")

    @commands.command()
    @commands.guild_only()
    @commands.is_owner()
    async def load_event_winners(
        self,
        ctx: commands.Context,
    ) -> None:
        winners_description = """<:1stplacecrown:1201249547737894972> Zueskin - <:fishing:1206108513630167100><:hunter:1206108328745508884><:mining:1206108388908474410> <:agility:1206107880743374879><:runecraft:1206043316441976842><:woodcutting:1206108707599945728><:slayer:1206108270323040256>
                Pepitabear - <:smithing:1206108441689591808> <:crafting:1206108122725351495><:ranged:1206043039974432778>
                Rotting - <:slayer:1206108270323040256><:herblore:1206107985076822076> 
                unrot - <:kq:1206109938888347718><:quizmaster:1206109857288032256>
                kitty neko - <:nex:1206109998883807242>
                Yoshe - <:giantmole:1206109787528364062>
                Kainsaw - <:mining:1206108388908474410>
                Adaboy23 - <:kbd:1206110064910532621>
                Assert - <:construction:1206043329498972173>
                w1zzy -  <:barrows:1206110138620973107>
                XtraIcy - <:slayer:1206108270323040256>
                Tonystano - <:barrows:1206110138620973107>
                Its Airalin - <:woodcutting:1206108707599945728>
                Sappx - <:woodcutting:1206108707599945728>
                Chompy bb - <:zulrah:1206110323346771968>
                Bornfury95 - <:inferno:1206110192450932828>
                sneaky uu - <:inferno:1206110192450932828>"""

        for i in range(ceil(len(winners_description) / 4096)):
            embed = discord.Embed(
                title="__Skilling & Bossing Event Winners__",
            )
            embed.description = winners_description[(4096 * i) : (4096 * (i + 1))]
            embed.set_thumbnail(
                url="https://oldschool.runescape.wiki/images/Stats_icon.png?1b467&20160515204513"
            )
            await ctx.send(embed=embed)

        embed.set_thumbnail(
            url="https://oldschool.runescape.wiki/images/Stats_icon.png?1b467&20160515204513"
        )

        embed = discord.Embed(title="Candyland (2023)")

        embed.add_field(
            name="",
            value="<:1stplacecrown:1201249547737894972> Impressed, Alchoholic, Helen Feller. Baked, A Cat Dad, Iron Coosa\n\nhttps://discord.com/channels/847313025919746129/847313574040305704/1097535747902423150",
            inline=False,
        )

        embed.set_thumbnail(
            url="https://oldschool.runescape.wiki/images/thumb/Purple_sweets_detail.png/120px-Purple_sweets_detail.png?41120"
        )
        embed.set_footer(text="April 17th, 2023")

        await ctx.send(embed=embed)

        embed = discord.Embed(title="Snakes & Ladders (2023)")

        embed.add_field(
            name="",
            value="<:1stplacecrown:1201249547737894972> Lamhirh, Dopamemes, Adaboy23, Scarlet x3, Zueskin, Rotting\n\nhttps://discord.com/channels/847313025919746129/847313574040305704/1131088765675380847",
            inline=False,
        )

        embed.set_thumbnail(
            url="https://oldschool.runescape.wiki/images/Ladders.png?b5be8&20150310211136"
        )

        await ctx.send(embed=embed)

        embed = discord.Embed(title="Battle of the Gods (2023)")

        embed.add_field(
            name="",
            value="<:1stplacecrown:1201249547737894972> Lilies, Steals, Bir d, justduff, jalals mane, Fat Cat, silly cowboy, Domimic, VirginRabbi, Shypu, Musei, LunasHowl, XtraIcy\n\nhttps://discord.com/channels/847313025919746129/847313574040305704/1148004422153158666",
            inline=False,
        )

        embed.set_thumbnail(
            url="https://oldschool.runescape.wiki/images/thumb/Zamorak%27s_statue_%28Slepe%29.png/122px-Zamorak%27s_statue_%28Slepe%29.png?7e7ee"
        )

        embed.set_footer(text="September 3rd, 2023")

        await ctx.send(embed=embed)

        embed = discord.Embed(title="Black Cat Halloween Bingo (2023)")

        embed.add_field(
            name="",
            value="<:1stplacecrown:1201249547737894972> Shovele, unrot, kitty neko, scarlet x3, Lil Yeeter, Miggy Spoon, Iron Yesu\n\nhttps://discord.com/channels/847313025919746129/847313574040305704/1165755681664667789",
            inline=False,
        )

        embed.set_thumbnail(
            url="https://oldschool.runescape.wiki/images/thumb/Cat_%28black%29.png/180px-Cat_%28black%29.png?1dfde"
        )

        embed.set_footer(text="October 22nd, 2023")

        await ctx.send(embed=embed)

        embed = discord.Embed(title="Zueskin's Dartboard (2024)")

        embed.add_field(
            name="",
            value="<:1stplacecrown:1201249547737894972> gee i wonder whos gonna win this one better leave it blank just in case",
            inline=False,
        )

        embed.set_footer(text="February 11th, 2024")

        embed.set_thumbnail(
            url="https://oldschool.runescape.wiki/images/thumb/Target_%28Ranging_Guild%29.png/150px-Target_%28Ranging_Guild%29.png?89891"
        )

        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(StaticEmbed(bot))
