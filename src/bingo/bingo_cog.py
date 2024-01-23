import json
import typing

import discord
from discord import app_commands
from discord.ext import commands

from bingo.dartboard import Dartboard
from bingo.embed_generate import generate_dartboard_task_embed


class SignupModal(discord.ui.Modal, title="Sign up for Bingo"):
    def __init__(self, channel: discord.abc.GuildChannel):
        """ """
        super().__init__()
        self.channel = channel

    name = discord.ui.TextInput(
        style=discord.TextStyle.short,
        label="username",
        required=True,
        placeholder="Enter the name of the character you wish to sign up",
    )

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.send_message(
            f"{self.name.value} is now signed up!", ephemeral=True
        )

        embed = discord.Embed(title="New Bingo Registration")
        embed.add_field(name="Discord User", value=f"{interaction.user.display_name}")
        embed.add_field(name="OSRS Name", value=f"{self.name.value}")

        message = await self.channel.send(embed=embed)
        await message.add_reaction("👍")
        await message.add_reaction("👎")

    async def on_error(self, interaction: discord.Interaction):
        await interaction.response.send_message(
            "Oops! Something went wrong.", ephemeral=True
        )


class Bingo(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.dartboard = Dartboard()

        with open("../config/appsettings.local.json") as settings_json:
            self.settings = json.load(settings_json)

    @app_commands.command()
    async def ping(self, interaction: discord.Interaction) -> None:
        ping1 = "500 ms"
        embed = discord.Embed(
            title="**Pong!**", description="**" + ping1 + "**", color=0xAFDAFC
        )
        await interaction.response.send_message(embed=embed)

    @app_commands.command()
    async def signup(self, interaction: discord.Interaction) -> None:
        channel = await self.bot.fetch_channel(self.settings["ApproveChannelId"])
        await interaction.response.send_modal(SignupModal(channel))

    @app_commands.command()
    async def change_paid_status(self, interaction: discord.Interaction) -> None:
        ping1 = f"{str(round(self.client.latency * 1000))} ms"
        embed = discord.Embed(
            title="**Pong!**", description="**" + ping1 + "**", color=0xAFDAFC
        )
        await interaction.response.send_message(embed=embed)

    @app_commands.command()
    async def clear_database(self, interaction: discord.Interaction) -> None:
        ping1 = f"{str(round(self.client.latency * 1000))} ms"
        embed = discord.Embed(
            title="**Pong!**", description="**" + ping1 + "**", color=0xAFDAFC
        )
        await interaction.response.send_message(embed=embed)

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


async def setup(bot):
    await bot.add_cog(Bingo(bot))
