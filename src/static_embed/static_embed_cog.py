import logging
from math import ceil
from static_embed.constants.player_names import PlayerNames 

import discord
from discord.ext import commands

import static_embed.embeds as embeds

class StaticEmbed(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.logger = logging.getLogger("discord")

    def is_bot(self, message):
        return message.author == self.bot.user

    @commands.Cog.listener()
    async def on_ready(self):
        self.logger.info("static embed cog loaded")

    @commands.command()
    @commands.guild_only()
    @commands.has_role("Admin")
    async def load_fun_stats(
        self,
        ctx: commands.Context,
    ) -> None:
        await ctx.channel.purge(check=self.is_bot)
        await ctx.send(embed=embeds.get_grandmasters_embed(), silent=True)
        await ctx.send(embed=embeds.get_fun_stats(), silent=True)
        await ctx.send(embed=embeds.get_200ms(), silent=True)
        await ctx.send(embed=embeds.get_clogs(), silent=True)
        await ctx.send(embed=embeds.get_tears(), silent=True)
        await ctx.message.delete()

    @commands.command()
    @commands.guild_only()
    @commands.has_role("Admin")
    async def load_submit_tutorial(
        self,
        ctx: commands.Context,
    ) -> None:
        embed = discord.Embed(
            title="✅ __**How to Submit a PB**__",
            description="Submitting a PB is split out into a couple different categories, and can be done with the following commands:\n```/submit tob\n/submit cox\n/submit toa\n/submit dt2\n/submit trials\n/submit boss\n/submit misc```\nLet the command autofill the available options. You need a saved screenshot of your PB.\nFor raids, your **entire** team must be clan members, and screenshots taken **inside** the raid.\nMust a clan member for 1 month+ before submitting (for raids, only one person needs this eligibility)",
            colour=0x94E1FF,
        )

        embed.set_thumbnail(
            url="https://oldschool.runescape.wiki/images/thumb/Platinum_speedrun_trophy_detail.png/120px-Platinum_speedrun_trophy_detail.png?0afd8"
        )

        await ctx.send(embed=embed)
        embed = discord.Embed(
            description="If there's any issues reach out to @Yoshe or @Zueskin.\nPlease do **not** type in this channel (other than using the commands)"
        )

        await ctx.send(embed=embed)

    @commands.command()
    @commands.guild_only()
    @commands.has_role("Admin")
    async def load_rules(
        self,
        ctx: commands.Context,
    ) -> None:
        embed = discord.Embed(
            title="Clan Rulebook",
            description="""**__General__**\n```• Change your Discord nickname to match your RSN\n• We are an English-speaking server\n• Be kind to everyone. A lot of events are welcome to guests/clan friends, so treat them with respect.\n• No gear shaming (fire cape, etc.) or showing toxicity towards gear or goals\n• No selfies or any information that can identify you IRL\n• Avoid political talk\n• Keep Runescape category channels on-topic (don't push up someone's #achievement with spam)\n• Please hide from the clan channel if deathmatching as we don't promote gambling
                      \n```\n__**Absolutely NO tolerance for:**__\n```ansi
                      \n\u001b[2;31m• NO WARNING - INSTANT BAN\u001b[0m\n• Harassing other clanmates (wilderness, etc)\n• Malicious links, scamming, doxing\n• Begging for gear loans or GP\n• Advertisement of non-Jagex compliant OSRS services\n• NSFW\n• Racism/hate speech```
                      \n__**DM an admin if you have any clan issues**__\nAlways double check you're not talking to an imposter account!
                      \n@yoshe_\n@kittycats.\n@adaboy23\n@chompybb\n@im_lavitz\n@thejeffz\n@southern_magician\n@infuse.\n@solstxce\n@unrot\n@zueskin
                      \nAbove all else, have fun and enjoy your time in the clan!""",
                      colour=0xad0000)

        embed.set_thumbnail(url="https://oldschool.runescape.wiki/images/thumb/Journal_%28Horror_from_the_Deep%29_detail.png/130px-Journal_%28Horror_from_the_Deep%29_detail.png?0752e")

        await ctx.send(embed=embed)

    @commands.command()
    @commands.guild_only()
    @commands.has_role("Admin")
    async def load_event_winners(
        self,
        ctx: commands.Context,
    ) -> None:
        winners_description = f"""
                <:1stplacecrown:1201249547737894972>{PlayerNames.zueskin} - <:fishing:1206108513630167100><:hunter:1206108328745508884><:mining:1206108388908474410> <:agility:1206107880743374879><:runecraft:1206043316441976842><:woodcutting:1206108707599945728><:slayer:1206108270323040256>
                {PlayerNames.pepitabear} - <:smithing:1206108441689591808> <:crafting:1206108122725351495><:ranged:1206043039974432778>
                {PlayerNames.rotting} - <:slayer:1206108270323040256><:herblore:1206107985076822076> 
                {PlayerNames.unrot} - <:kq:1206109938888347718><:quizmaster:1206109857288032256>
                {PlayerNames.neko} - <:nex:1206109998883807242>
                {PlayerNames.yoshe} - <:giantmole:1206109787528364062>
                {PlayerNames.kainsaw} - <:mining:1206108388908474410>
                {PlayerNames.adaboy} - <:kbd:1206110064910532621>
                {PlayerNames.assert_rs} - <:construction:1206043329498972173>
                {PlayerNames.w1zzy} -  <:barrows:1206110138620973107>
                {PlayerNames.pepitabear} - <:slayer:1206108270323040256>
                {PlayerNames.tonystano} - <:barrows:1206110138620973107>
                {PlayerNames.its_airalin} - <:woodcutting:1206108707599945728>
                {PlayerNames.sappx} - <:woodcutting:1206108707599945728>
                {PlayerNames.chompy} - <:zulrah:1206110323346771968>
                {PlayerNames.bornfury95} - <:inferno:1206110192450932828>
                {PlayerNames.sneaky} - <:inferno:1206110192450932828>
                {PlayerNames.crayy} - <:orb:1215861831156105317>
                {PlayerNames.mustard_mommy} - <:orb:1215861831156105317>
                {PlayerNames.jeffke_12} - <:orb:1215861831156105317>
                {PlayerNames.pup_in_a_cup} - <:orb:1215861831156105317>"""

        # Gets around the 1024 character limit by chunking the request
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
        await ctx.send(embed=embeds.get_dartboard_embed())


async def setup(bot):
    await bot.add_cog(StaticEmbed(bot))
