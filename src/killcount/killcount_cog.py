import logging
import asyncio
import discord
from discord.ext import tasks, commands
from constants.channels import ChannelIds
from datetime import time
from constants.timezone import Eastern_Standard_Timezone
from killcount.constants.groups import BossGroups

MIDNIGHT_EST = time(hour=0, minute=0, second=0, tzinfo=Eastern_Standard_Timezone)


class KillCount(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.logger = logging.getLogger("discord")

    @commands.Cog.listener()
    async def on_ready(self):
        self.logger.info("management cog loaded")

    @commands.command()
    @commands.is_owner()
    async def manual_update_killcount(self, ctx: commands.Context):
        pass

    @tasks.loop(time=MIDNIGHT_EST)  # <- will do this every 5 seconds
    async def auto_update_killcount(self, *args):
        pass

    async def update_killcount(self):
        embeds = [self.embed_generator(group) for group in BossGroups]
        # TODO: clear channel
        # TODO: send message with embeds

    async def embed_generator(self, group):
        # TODO: make embeds
        pass

        

async def setup(bot):
    await bot.add_cog(KillCount(bot))
