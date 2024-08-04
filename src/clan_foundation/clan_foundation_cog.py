import logging
import discord
import clan_foundation.embeds as embeds
from discord import app_commands
from discord.ext import commands

class HelpView(discord.ui.View):
    """
    Help Button
    """
    @discord.ui.button(
        label="❗Help",
        style=discord.ButtonStyle.secondary,
    )
    async def send_rules(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("Help is on the way!", ephemeral=True)
    
    @discord.ui.button(
        label="⚠️ Report a player",
        style=discord.ButtonStyle.secondary,
    )
    async def send_report(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("Help is on the way!", ephemeral=True)

class WelcomeView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
    
    """
    Rules Button
    """
    @discord.ui.button(
        label="📒Rules",
        style=discord.ButtonStyle.secondary,
    )
    async def send_rules(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(embed=await embeds.draw_clan_rules_embed(), ephemeral=True)
    
    """
    Staff Button
    """
    @discord.ui.button(
        label="🔑 Staff",
        style=discord.ButtonStyle.secondary,
    )
    async def send_staff(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(embed=await embeds.draw_staff_embed(), ephemeral=True, view=HelpView())
    
    """
    How to Join Button
    """
    @discord.ui.button(
        label="❓ How to Join",
        style=discord.ButtonStyle.secondary,
    )
    async def send_how_to_join(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("You clicked the how to join button", ephemeral=True)

    """
    Ranking System Button
    """
    @discord.ui.button(
            label="🏆 Ranking System",
            style=discord.ButtonStyle.secondary,
    )
    async def send_ranking_system(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("You clicked the ranking system button", ephemeral=True)

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

    @app_commands.command(name="foundation_setup_clanranks")
    @app_commands.checks.has_role("Admin")
    async def admin_welcome_setup(
        self,
        interaction: discord.Interaction,
    ) -> None:
        await interaction.channel.send(embed=await embeds.draw_clan_profile_embed())

    @app_commands.command(name="foundation_setup_welcome")
    @app_commands.checks.has_role("Admin")
    async def admin_submission_setup(
        self,
        interaction: discord.Interaction,
    ) -> None:
        await interaction.channel.send(embed=await embeds.draw_clan_foundation_embed(), view=WelcomeView())  


        
async def setup(bot):
    await bot.add_cog(ClanFoundation(bot))