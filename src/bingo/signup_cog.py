import json
import typing

import discord
from discord import app_commands
from discord.ext import commands

import logging


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


class Signup(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.is_registration_open = False

        with open("../config/appsettings.local.json") as settings_json:
            self.settings = json.load(settings_json)

    @app_commands.command(name="signup", description="Signup form for bingo")
    async def signup(self, interaction: discord.Interaction) -> None:
        if self.is_registration_open:
            channel = await self.bot.fetch_channel(self.settings["ApproveChannelId"])
            await interaction.response.send_modal(SignupModal(channel))
        else:
            await interaction.response.send_message(
                "Sign up is currently closed", ephemeral=True
            )

    @commands.command()
    @commands.is_owner()
    async def toggle_signup(self, ctx: commands.Context):
        self.is_registration_open = not self.is_registration_open
        ternary = "enable" if self.is_registration_open else "disabled"
        await ctx.send(f"Signups have been {ternary}")

    @app_commands.command()
    async def change_paid_status(self, interaction: discord.Interaction) -> None:
        ping1 = f"{str(round(self.bot.latency * 1000))} ms"
        embed = discord.Embed(
            title="**Pong!**", description="**" + ping1 + "**", color=0xAFDAFC
        )
        await interaction.response.send_message(embed=embed)

    @app_commands.command()
    async def clear_database(self, interaction: discord.Interaction) -> None:
        ping1 = f"{str(round(self.bot.latency * 1000))} ms"
        embed = discord.Embed(
            title="**Pong!**", description="**" + ping1 + "**", color=0xAFDAFC
        )
        await interaction.response.send_message(embed=embed)

    @commands.Cog.listener()
    async def on_ready(self):
        logger = logging.getLogger('discord')
        logger.critical("signup cog loaded")

async def setup(bot):
    await bot.add_cog(Signup(bot))
