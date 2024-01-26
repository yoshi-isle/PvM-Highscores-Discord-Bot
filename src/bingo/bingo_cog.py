import logging
import typing

import discord
from discord import app_commands
from discord.ext import commands

from bingo.dartboard import Dartboard
from bingo.embed_generate import generate_dartboard_task_embed

team_names = ["Sapphire",
            "Ruby",
            "Emerald",
            "Diamond",
            "Dragonstone",
            "Opal",
            "Jade",
            "Topaz",
            ]


class Bingo(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.logger = logging.getLogger("discord")
        self.dartboard = Dartboard()
        self.is_registration_open = False

    async def throw_a_dart_autocomplete(
        self,
        interaction: discord.Interaction,
        current: str,
    ) -> typing.List[app_commands.Choice[str]]:
        
        return [app_commands.Choice(name=team_name, value=team_name) for team_name in team_names if current.lower() in team_name.lower()]

    @app_commands.command(name="throw_a_dart")
    @app_commands.describe(team="Generate a new task for your team")
    @app_commands.autocomplete(team=throw_a_dart_autocomplete)
    async def throw_a_dart(
        self,
        interaction: discord.Interaction,
        team: str,
    ):
        new_task = self.dartboard.get_task()
        embed = await generate_dartboard_task_embed(
            team_name=f"{team}",
            task=new_task,
        )

        await interaction.response.send_message(embed=embed)

    @commands.Cog.listener()
    async def on_ready(self):
        self.logger.critical("bingo cog loaded")


async def setup(bot):
    await bot.add_cog(Bingo(bot))
