import logging

import discord
from discord.ext import commands
from management.random_greeting import get_random_greeting_url


class NewMemberView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(
        label="Wave to say Meowdy!",
        style=discord.ButtonStyle.secondary,
    )
    async def send_gif(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        embed = discord.Embed()
        greetings = " says..."
        embed.set_author(
            name=interaction.user.display_name + greetings,
            icon_url=interaction.user.display_avatar.url,
        )
        embed.set_image(url=await get_random_greeting_url())
        await interaction.response.send_message(embed=embed)


class Greetings(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.logger = logging.getLogger("discord")

    @commands.Cog.listener()
    async def on_ready(self):
        self.logger.info("greetings cog loaded")

    @commands.Cog.listener()
    async def on_member_join(self, member):
        guild = member.guild
        if guild.system_channel is not None:
            to_send = f"Welcome {member.mention} to {guild.name}!"
            await guild.system_channel.send(to_send, view=NewMemberView())


async def setup(bot):
    await bot.add_cog(Greetings(bot))
