import logging
import discord
from discord.ext import commands
from math import ceil
import static_embed.embeds as embeds


class StaticEmbed(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.logger = logging.getLogger("discord")

    @commands.Cog.listener()
    async def on_ready(self):
        self.logger.info("static embed cog loaded")

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
                cat nya - <:nex:1206109998883807242>
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
            embed.set_thumbnail(url="https://oldschool.runescape.wiki/images/Stats_icon.png?1b467&20160515204513")
            await ctx.send(embed=embed)

        await ctx.send(embed=embeds.get_candyland_embed())
        await ctx.send(embed=embeds.get_snakeandladders_embed())
        await ctx.send(embed=embeds.get_battleofgods_embed())
        await ctx.send(embed=embeds.get_blackcatbingo_embed())
        # await ctx.send(embed=embeds.get_dartboard_embed())


async def setup(bot):
    await bot.add_cog(StaticEmbed(bot))
