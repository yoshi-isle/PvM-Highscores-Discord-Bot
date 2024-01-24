import json
import logging

import discord
from discord import app_commands
from discord.ext import commands



class SignupView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label='Signup', style=discord.ButtonStyle.primary, custom_id='persistent_view:signup')
    async def signup(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(SignupModal(interaction.channel))
        
    

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
        self.logger = logging.getLogger("discord")

        with open("../config/appsettings.local.json") as settings_json:
            self.settings = json.load(settings_json)
        

    @commands.command()
    @commands.is_owner()
    async def toggle_signup(self, ctx: commands.Context):
        discord.ui.Button
        self.registration_status.is_open = not self.registration_status.is_open
        ternary = "enable" if self.registration_status.is_open else "disabled"
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
        self.logger.critical("signup cog loaded")

    @commands.command()
    @commands.is_owner()
    async def prepare(self, ctx: commands.Context):
        """Starts a persistent view."""
        # In order for a persistent view to be listened to, it needs to be sent to an actual message.
        # Call this method once just to store it somewhere.
        # In a more complicated program you might fetch the message_id from a database for use later.
        # However this is outside of the scope of this simple example.
        embed = discord.Embed(title="What is a Bingo?",
                      description="```\nClan bingos are events where teams aim to collect specific items for points. Prizes will be given out at the end of the event to the teams with the most points. While the events may vary slightly each time, the overall concept remains consistent.\n\nAnnouncements for bingos typically occur two weeks in advance and bingos run for about a week. \n\nSign-ups open immediately after the announcement and close just before team formation. After signing up, admins will prompt participants in the chat to gather the entry fee at the GE on world 354, contributing to the prize pool. \n\nA day or two before the bingo begins, the team-making event takes place. This can involve random captains selecting teams in a draft style or through a random process. Once teams are formed, a dedicated Discord channel is created for each team to plan and communicate. \n\nThe primary goal is to have fun, bond with clan mates, and explore new content that you might not have tried otherwise.\n```",
                      colour=0x234d4a)

        embed.set_author(name="Bingo Info")

        embed.add_field(name="Buy in Amount",
                        value="5m gp",
                        inline=False)
        embed.add_field(name="Registration dates",
                        value="Open from <t:1706080980:d> to <t:1706080980:d>",
                        inline=True)
        embed.add_field(name="Bingo Dates",
                        value="Open from <t:1706080980:d> to <t:1706080980:d>",
                        inline=False)

        embed.set_image(url="https://cdn.discordapp.com/attachments/1135573799790723082/1142889311738531891/image.png?ex=65bfd89d&is=65ad639d&hm=29abbc35d89b6746e50b567596f5709605169a7bf789f1f05977659327016ab0&")

        embed.set_thumbnail(url="https://media.discordapp.net/attachments/1135573799790723082/1157440713286484079/Screenshot_77.png?ex=65bd69aa&is=65aaf4aa&hm=c3e5cf17fcdb3d89be529c0bf34bba10d0c43d56b34753b806017aca8f116d95&=&format=webp&quality=lossless&width=1080&height=590")

        embed.set_footer(text="Example Footer")

        await ctx.send(embed=embed,view=SignupView())

async def setup(bot):
    await bot.add_cog(Signup(bot))
