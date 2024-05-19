import logging
from discord import app_commands
from discord.ext import commands


class Summerland(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.logger = logging.getLogger("discord")
        self.database = self.bot.database

    @commands.Cog.listener()
    async def on_ready(self):
        self.logger.info("summerland cog loaded")

    @commands.command()
    async def hi(
        self,
        ctx: commands.Context,
    ) -> None:
        await ctx.send("hi")


async def setup(bot):
    await bot.add_cog(Summerland(bot))
