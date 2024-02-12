import logging
from datetime import time

import discord
from discord.ext import commands, tasks

from constants.channels import ChannelIds
from killcount.constants.groups import all_boss_groups

MIDNIGHT_EST = time(hour=0, minute=0, second=0, tzinfo=None)
NORMIE_ICON = "<:main:1206053914873565266>"
IRON_ICON = "<:ironman:1206051054270029876>"
YOSHE_ICON = "<:3apick:1149506028715659366>"


class KillCount(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.logger = logging.getLogger("discord")

    @commands.Cog.listener()
    async def on_ready(self):
        self.logger.info("killcount cog loaded")

    @commands.command()
    @commands.has_role("Admin")
    async def manual_update_killcount(self, ctx: commands.Context):
        await ctx.send("Updating killcounts")
        await self.update_killcount()

    @tasks.loop(time=MIDNIGHT_EST)  # will do this everynight at 12pm est
    async def auto_update_killcount(self, *args):
        await self.update_killcount()

    async def update_killcount(self):
        thread = self.bot.get_channel(ChannelIds.killcount_thread)
        embeds = [await self.embed_generator(group) for group in all_boss_groups]
        await thread.purge()
        for embed in embeds:
            await thread.send(embed=embed)

    async def embed_generator(self, group):
        embed = discord.Embed(title=f"{group.name}", description="")

        embed.set_thumbnail(url=group.url)
        for boss in group.bosses:
            # convert the internal name from snake case to normal capitalization
            boss_name = " ".join([word.capitalize() for word in boss.value.split("_")])
            normies, irons = await self.bot.wom.get_top_placements_hiscores(metric=boss)
            normie_icon = NORMIE_ICON
            if normies[0].player.display_name == "yoshe":
                normie_icon = YOSHE_ICON
            normie = normie_icon + f" {normies[0].player.display_name} - {normies[0].data.kills} KC"
            iron = IRON_ICON + f" {irons[0].player.display_name} - {irons[0].data.kills} KC\n"

            embed.add_field(name=f" __{boss_name}__", value=normie + "\n" + iron, inline=False)

        return embed


async def setup(bot):
    await bot.add_cog(KillCount(bot))
