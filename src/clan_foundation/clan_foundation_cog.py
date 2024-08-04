import logging
import discord
from discord import Embed, app_commands
from discord.ext import commands
from discord.ui import Button
from discord.ui import View

class ClanFoundation(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.logger = logging.getLogger("discord")
        self.database = self.bot.database
        self.cooldown = 20
        self.last_used = 0
    

    @commands.Cog.listener()
    async def on_ready(self):
        self.logger.info("clan foundation cog loaded")

    @app_commands.command(name="clan_profile")
    async def view_clan_profile(
        self,
        interaction: discord.Interaction,
    ) -> None:
        channel = interaction.guild.get_channel(interaction.channel_id)
        await channel.send("Pong")

        
async def setup(bot):
    await bot.add_cog(ClanFoundation(bot))