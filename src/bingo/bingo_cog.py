import json
import typing

import discord
from discord import app_commands
from discord.ext import commands

from bingo.dartboard import Dartboard
from bingo.embed_generate import generate_dartboard_task_embed
import logging


class Bingo(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.dartboard = Dartboard()
        self.is_registration_open = False

        with open("../config/appsettings.local.json") as settings_json:
            self.settings = json.load(settings_json)

    async def throw_a_dart_autocomplete(
        self,
        interaction: discord.Interaction,
        current: str,
    ) -> typing.List[app_commands.Choice[str]]:
        data = []
        for team_name in [
            "Sapphire",
            "Ruby",
            "Emerald",
            "Diamond",
            "Dragonstone",
            "Opal",
            "Jade",
            "Topaz",
        ]:
            if current.lower() in team_name.lower():
                data.append(app_commands.Choice(name=team_name, value=team_name))
        return data

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
        logger = logging.getLogger('discord')
        logger.critical("bingo cog loaded")


async def setup(bot):
    await bot.add_cog(Bingo(bot))
