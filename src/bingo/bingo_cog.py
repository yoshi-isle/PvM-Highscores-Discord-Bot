import logging
import typing

import discord
from discord import app_commands
from discord.ext import commands

from bingo.constants import team_names
from bingo.dartboard import Dartboard
from bingo.embed_generate import generate_dartboard_task_embed
from constants.channels import ChannelIds


class Bingo(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.logger = logging.getLogger("discord")
        self.dartboard = Dartboard()

    async def throw_a_dart_autocomplete(
        self,
        interaction: discord.Interaction,
        current: str,
    ) -> typing.List[app_commands.Choice[str]]:
        return [app_commands.Choice(name=team_name, value=team_name) for team_name in team_names.team_names if current.lower() in team_name.lower()]

    @app_commands.command(name="throw_a_dart")
    @app_commands.describe(team="Generate a new task for your team")
    @app_commands.autocomplete(team=throw_a_dart_autocomplete)
    @app_commands.checks.has_role("Darts 2024")
    async def throw_a_dart(
        self,
        interaction: discord.Interaction,
        team: str,
    ):
        dart_channel = self.bot.get_channel(ChannelIds.dartboard_commands)
        if dart_channel is None:
            self.logger.warning("%s could not be found. Did you update constants.channel_ids?" % dart_channel)
        else:
            new_task = self.dartboard.get_task()
            embed = await generate_dartboard_task_embed(
                team_name=team,
                task=new_task,
            )

            self.logger.info(f"{team} rolled {new_task}")

            rolled = " rolled..."
            embed.set_author(name=interaction.user.display_name + rolled, icon_url=interaction.user.display_avatar.url)

            message = await dart_channel.send(embed=embed)
            await interaction.response.send_message(
                f"Generated a new task for you! {message.to_reference().jump_url}",
                ephemeral=True,
            )

    @commands.Cog.listener()
    async def on_ready(self):
        self.logger.info("bingo cog loaded")


async def setup(bot):
    await bot.add_cog(Bingo(bot))
