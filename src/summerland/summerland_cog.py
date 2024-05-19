import logging
from discord import app_commands
from discord.ext import commands
import json


class Summerland(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.logger = logging.getLogger("discord")
        self.database = self.bot.database

    @commands.Cog.listener()
    async def on_ready(self):
        self.logger.info("summerland cog loaded")

    @commands.command()
    async def temp_updatetile(
        self,
        ctx: commands.Context,
        tile: int,
    ) -> None:
        await ctx.send(f"Going to tile {tile}")
        await self.database.update_team_tile(
            "1241499583180177469", "current_tile", tile
        )
        record = await self.database.get_team_info("1241499583180177469")

        current = record["tile_history"]
        print(current)
        current.append(tile)
        print(current)
        await self.database.update_team_tile(
            "1241499583180177469", "tile_history", current
        )


async def setup(bot):
    await bot.add_cog(Summerland(bot))
