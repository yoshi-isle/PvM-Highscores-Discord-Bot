import logging
from dataclasses import dataclass
from typing import List

import discord
from discord import app_commands
from discord.ext import commands
from table2ascii import table2ascii as t2a


@dataclass(frozen=False)
class SignupEntry:
    discord_name: str
    osrs_username: str
    team_mates: List[str]


class SignupView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(
        label="Signup",
        style=discord.ButtonStyle.primary,
        custom_id="persistent_view:signup",
    )
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
        entry = SignupEntry(
            discord_name=interaction.user.display_name,
            osrs_username=self.name.value,
            team_mates=[""],
        )

        id = await interaction.client.database.new_signup(entry)

        await interaction.response.send_message(
            f"{self.name.value} is now signed up!", ephemeral=True
        )

        embed = discord.Embed(title="New Bingo Registration")
        embed.add_field(name="Discord User", value=f"{interaction.user.display_name}")
        embed.add_field(name="OSRS Name", value=f"{self.name.value}")

        message = await self.channel.send(embed=embed)

    async def on_error(self, interaction: discord.Interaction):
        await interaction.response.send_message(
            "Oops! Something went wrong.", ephemeral=True
        )


class Signup(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.logger = logging.getLogger("discord")
        self.database = self.bot.database

    async def entry_complete(
        self,
        interaction: discord.Interaction,
        current: str,
    ) -> List[app_commands.Choice[str]]:
        data = self.database.signup_collection.find({},{ "osrs name": 1, "paid": 1})
        names = [doc["osrs name"] for doc in data if not doc["paid"]]
        return [
            app_commands.Choice(name=name, value=name)
            for name in names
            if current.lower() in name.lower()
        ]

    @app_commands.command()
    @app_commands.autocomplete(name=entry_complete)
    async def change_paid_status(self, 
                                 interaction: discord.Interaction,
                                 name : str,
                                 paid : bool,) -> None:  
        entry = {"osrs name": name}
        new_paid = {"$set" :{"paid": paid}}
        self.database.signup_collection.update_one(entry,new_paid)
        await interaction.response.send_message(f"{name}")

    @commands.command()
    async def clear_database(self, ctx: commands.Context) -> None:
        self.database.signup_collection.delete_many({})
        await ctx.send("data base cleared")

    @commands.command()
    @commands.has_role("Admin")
    async def close_signups(self, ctx: commands.Context):
        bingo_message = self.database.mgmt_collection.find_one()
        if bingo_message.get("message id"):
            signup_message = await ctx.fetch_message(bingo_message.get("message id"))
            await discord.Message.delete(signup_message)
            self.database.mgmt_collection.delete_one(bingo_message)

    @commands.command()
    @commands.has_role("Admin")
    async def generate_signups(self, ctx: commands.Context):
        entries = self.database.signup_collection.find()
        keys_to_extract = [
            "discord name",
            "osrs name",
            "team mates",
            "paid",
            "paid proof cdn",
        ]
        data = [[doc[key] for key in keys_to_extract] for doc in entries]
        output = t2a(
            header=["Discord Name", "OSRS Name", "Teammates", "Paid", "url"],
            body=data,
            first_col_heading=True,
        )

        await ctx.send(f"```\n{output}\n```")

    @commands.command()
    @commands.has_role("Admin")
    async def static_bingo(self, ctx: commands.Context):
        await ctx.message.delete()
        embed = discord.Embed(
            title="What is a Bingo?",
            description="```\nClan bingos are events where teams aim to collect specific items for points. Prizes will be given out at the end of the event to the teams with the most points. While the events may vary slightly each time, the overall concept remains consistent.\n\nAnnouncements for bingos typically occur two weeks in advance and bingos run for about a week. \n\nSign-ups open immediately after the announcement and close just before team formation. After signing up, admins will prompt participants in the chat to gather the entry fee at the GE on world 354, contributing to the prize pool. \n\nA day or two before the bingo begins, the team-making event takes place. This can involve random captains selecting teams in a draft style or through a random process. Once teams are formed, a dedicated Discord channel is created for each team to plan and communicate. \n\nThe primary goal is to have fun, bond with clan mates, and explore new content that you might not have tried otherwise.\n```",
            colour=0x234D4A,
        )

        await ctx.send(embed=embed)

    @commands.command()
    @commands.has_role("Admin")
    async def create_signup(
        self,
        ctx: commands.Context,
    ):
        """Starts a persistent view."""

        await ctx.message.delete()
        embed = discord.Embed(
            title="Event Title?",
            description="```Event Description```",
            colour=0x234D4A,
        )
        embed.set_author(name="Bingo Info")
        embed.add_field(name="Buy in Amount", value="5m gp", inline=False)
        embed.add_field(
            name="Registration dates",
            value="Open from <t:1706080980:d> to <t:1706080980:d>",
            inline=True,
        )
        embed.add_field(
            name="Bingo Dates",
            value="Open from <t:1706080980:d> to <t:1706080980:d>",
            inline=False,
        )
        embed.set_image(
            url="https://cdn.discordapp.com/attachments/1135573799790723082/1142889311738531891/image.png?ex=65bfd89d&is=65ad639d&hm=29abbc35d89b6746e50b567596f5709605169a7bf789f1f05977659327016ab0&"
        )
        embed.set_thumbnail(
            url="https://media.discordapp.net/attachments/1135573799790723082/1157440713286484079/Screenshot_77.png?ex=65bd69aa&is=65aaf4aa&hm=c3e5cf17fcdb3d89be529c0bf34bba10d0c43d56b34753b806017aca8f116d95&=&format=webp&quality=lossless&width=1080&height=590"
        )
        embed.set_footer(text="Example Footer")

        message = await ctx.send(embed=embed, view=SignupView())
        await self.bot.database.add_persistent_message_id(message.id)

    @commands.Cog.listener()
    async def on_ready(self):
        self.logger.info("signup cog loaded")


async def setup(bot):
    await bot.add_cog(Signup(bot))
