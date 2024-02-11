import logging
import asyncio
import discord
from discord.ext import tasks, commands
from constants.channels import ChannelIds
from datetime import time
from constants.timezone import Eastern_Standard_Timezone
from killcount.constants.groups import all_boss_groups

MIDNIGHT_EST = time(hour=0, minute=0, second=0, tzinfo=None)


class KillCount(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.logger = logging.getLogger("discord")

    @commands.Cog.listener()
    async def on_ready(self):
        self.logger.info("killcount cog loaded")

    @commands.command()
    @commands.is_owner()
    async def manual_update_killcount(self, ctx: commands.Context):
        await self.update_killcount()

    @tasks.loop(time=MIDNIGHT_EST)  # <- will do this every 5 seconds
    async def auto_update_killcount(self, *args):
        await self.update_killcount()

    async def update_killcount(self, ctx):
        channel = self.get_channel()
        embeds = [await self.embed_generator(group) for group in all_boss_groups]
        await channel.purge()
        await channel.send(embeds=embeds)
        

    async def embed_generator(self, group):
        embed = discord.Embed(title=f"{group.name}",
                      description="test description for body")

        embed.set_thumbnail(url=group.url)
        for boss in group.bosses:
            # convert the internal name from snake case to normal capitalization
            boss_name = " ".join([word.capitalize() for word in boss.value.split('_')])
            normies, irons = await self.bot.wom.get_top_placements_hiscores(metric=boss)
            normie = f"{normies[0].player.display_name} - {normies[0].data.kills}"
            iron = f"Ironman: {irons[0].player.display_name} - {irons[0].data.kills}"

            embed.add_field(name=f"{boss_name}",
                            value=normie + "\n" + iron,
                            inline=False)
            
        return embed


        

async def setup(bot):
    await bot.add_cog(KillCount(bot))
