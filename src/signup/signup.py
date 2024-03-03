import logging
from dataclasses import dataclass
from typing import List, Tuple

import discord
from discord import app_commands
from discord.ext import commands
from table2ascii import table2ascii as t2a
from database import Database

@dataclass(frozen=False)
class SignupEntry:
    discord_name: str
    osrs_username: str
    team_mates: List[str]


async def build_signup_tables(database: Database):
    """Calls the mongo database and returns 2 tables for the unpaid and paid statuses of currently signed up members

    Args:
        database: Mongo Database to connect to

    Returns:
        _type_: Two tables with unpaid and paid entries
    """
    entries = database.signup_collection.find()
    keys_to_extract = [
        "discord name",
        "osrs name",
        "team mates",
        "paid",
    ]
    data = [[doc[key] for key in keys_to_extract] for doc in entries]

    true_rows = []
    false_rows = []

    for sublist in data:
        if sublist[3]:  # Check if the fourth element is True
            true_rows.append(sublist)
        else:
            false_rows.append(sublist)

    true_table = t2a(
        header=["Discord Name", "OSRS Name", "Teammates"],
        body=[row[:3] for row in true_rows],
        first_col_heading=True,
    )

    false_table = t2a(
        header=["Discord Name", "OSRS Name", "Teammates"],
        body=[row[:3] for row in false_rows],
        first_col_heading=True,
    )

    return false_table, true_table

async def update_signup_tables(database: Database, channel):
    false_table, true_table = await build_signup_tables(database)

    false = database.mgmt_collection.find_one({"message_key": "false table"})
    false_table_message = await channel.fetch_message(
        false.get("message id")
    )
    await false_table_message.edit(
        content=f"```ansi\n[2;31mUNPAID\n{false_table}[0m\n```"
    )

    true = database.mgmt_collection.find_one({"message_key": "true table"})
    true_table_message = await channel.fetch_message(
        true.get("message id")
    )
    await true_table_message.edit(
        content=f"```ansi\n[2;36mPAID\n{true_table}[0m\n```"
    )

class WithdrawView(discord.ui.View):
    """Button intended as an ephermeral confirmation. Will remove player based on display name and update tables
    """
    def __init__(self, player):
        super().__init__(timeout=20) # times out in 20 seconds
        self.player=player

    @discord.ui.button(
        label="Yes",
        style=discord.ButtonStyle.red)
    async def withdraw(self, interaction: discord.Interaction, button: discord.ui.Button):
        interaction.client.database.signup_collection.delete_one(self.player)
        signup = interaction.client.database.mgmt_collection.find_one(
            {"message_key": "signup thread"}
        )
        signup_thread = await interaction.client.fetch_channel(signup.get("message id"))

        paid_status_text = "They did not pay yet"
        if self.player.get('paid'):    
            paid_status_text = "They had paid"

        await signup_thread.send(f"{interaction.user.display_name} withdrew from the event. {paid_status_text}")

        await interaction.response.send_message("You have been removed from the event", ephemeral=True, delete_after=20)

        await update_signup_tables(interaction.client.database, interaction.channel)

class SignupView(discord.ui.View):
    """Persistent view that is used to display the sign up modal and withdraw button

    Args:
        discord (_type_): _description_
    """
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(
        label="Signup",
        style=discord.ButtonStyle.primary,
        custom_id="persistent_view:signup",)
    async def signup(self, interaction: discord.Interaction, button: discord.ui.Button):
        player = interaction.client.database.signup_collection.find_one(
            {"discord name": interaction.user.display_name}
        )
        if player:
            await interaction.response.send_message(f"You are already signed up as {player.get('osrs name')}", ephemeral=True, delete_after=20)
        else:
            modal = SignupModal(interaction.channel)
            modal.name.default = interaction.user.display_name
            await interaction.response.send_modal(modal)

    @discord.ui.button(
        label="Withdraw",
        style=discord.ButtonStyle.grey,
        custom_id="persistent_view:withdraw",)
    async def withdraw(self, interaction: discord.Interaction, button: discord.ui.Button):
        player = interaction.client.database.signup_collection.find_one(
            {"discord name": interaction.user.display_name}
        )
        if player:
            await interaction.response.send_message("Are you sure you want to withdraw?", view=WithdrawView(player=player), ephemeral=True, delete_after=20)
        else:
            await interaction.response.send_message("You are not currently signed up", ephemeral=True,delete_after=20)


class SignupModal(discord.ui.Modal, title="Sign up for Bingo"):
    """Modal used for signing up. Sends entry to mongodb

    Args:
        discord (_type_): _description_
        title (str, optional): _description_. Defaults to "Sign up for Bingo".
    """
    def __init__(self, channel: discord.abc.GuildChannel):
        """ """
        super().__init__()
        self.channel = channel

    name = discord.ui.TextInput(
        style=discord.TextStyle.short,
        label="username",
        required=True,
        placeholder="Enter the name of the character you wish to sign up",
        max_length=13,
    )

    async def on_submit(self, interaction: discord.Interaction):
        entry = SignupEntry(
            discord_name=interaction.user.display_name,
            osrs_username=self.name.value,
            team_mates=[""],
        )

        id = await interaction.client.database.new_signup(entry)

        await interaction.response.send_message(
            f"{self.name.value} is now signed up!", ephemeral=True, delete_after=20
        )

        embed = discord.Embed(title="New Bingo Registration")
        embed.add_field(name="Discord User", value=f"{interaction.user.display_name}")
        embed.add_field(name="OSRS Name", value=f"{self.name.value}")
        signup = interaction.client.database.mgmt_collection.find_one(
            {"message_key": "signup thread"}
        )
        signup_thread = await interaction.client.fetch_channel(signup.get("message id"))

        await update_signup_tables(interaction.client.database, interaction.channel)

        message = await signup_thread.send(embed=embed)

    async def on_error(self, interaction: discord.Interaction):
        await interaction.response.send_message(
            "Oops! Something went wrong.", ephemeral=True
        )


class Signup(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.logger = logging.getLogger("discord")
        self.database = self.bot.database

    async def unpaid_entry_complete(
        self,
        interaction: discord.Interaction,
        current: str,
    ) -> List[app_commands.Choice[str]]:
        data = self.database.signup_collection.find({}, {"osrs name": 1, "paid": 1})
        names = [doc["osrs name"] for doc in data if doc["paid"]]
        return [
            app_commands.Choice(name=name, value=name)
            for name in names
            if current.lower() in name.lower()
        ]

    async def paid_entry_complete(
        self,
        interaction: discord.Interaction,
        current: str,
    ) -> List[app_commands.Choice[str]]:
        data = self.database.signup_collection.find({}, {"osrs name": 1, "paid": 1})
        names = [doc["osrs name"] for doc in data if not doc["paid"]]
        return [
            app_commands.Choice(name=name, value=name)
            for name in names
            if current.lower() in name.lower()
        ]

    async def change_paid_status(
        self,
        interaction: discord.Interaction,
        name: str,
        paid: bool,
    ):
        entry = {"osrs name": name}
        new_paid = {"$set": {"paid": paid}}
        player = self.database.signup_collection.find_one(entry)
        if not player:
            self.logger.error(f"player {name} was not in the signup database")
            return False

        if player["paid"] == paid:
            self.logger.error(f"player {name}'s status was already set to {paid}")
            return False

        update = self.database.signup_collection.update_one(entry, new_paid)
        await update_signup_tables(self.database, interaction.channel)

        return update

    @app_commands.command()
    @app_commands.autocomplete(name=paid_entry_complete)
    async def paid(
        self, interaction: discord.Interaction, name: str, image: discord.Attachment
    ) -> None:
        status = await self.change_paid_status(interaction, name, True)
        if status:
            payment = interaction.client.database.mgmt_collection.find_one(
                {"message_key": "payment thread"}
            )
            signup_thread = await interaction.client.fetch_channel(
                payment.get("message id")
            )
            await signup_thread.send(
                f"{interaction.user.mention} has submitted proof that **{name}** was paid for {image.url}"
            )
            await interaction.response.send_message("Successfully submitted", ephemeral=True)
        else:
            await interaction.response.send_message(
                "There was an error. Check the name or that you used the correct command",
                ephemeral=True,
            )

    @app_commands.command()
    @app_commands.autocomplete(name=unpaid_entry_complete)
    async def unpaid(
        self,
        interaction: discord.Interaction,
        name: str,
    ) -> None:
        status = await self.change_paid_status(interaction, name, False)
        if status:
            payment = interaction.client.database.mgmt_collection.find_one(
                {"message_key": "payment thread"}
            )
            signup_thread = await interaction.client.fetch_channel(
                payment.get("message id")
            )
            await signup_thread.send(
                f"{interaction.user.mention} has changed **{name}** to unpaid"
            )
            await interaction.response.send_message("successful submit", ephemeral=True)
        else:
            await interaction.response.send_message(
                "There was an error. Check the name or that you used the correct command",
                ephemeral=True,
            )

    @commands.command()
    async def clear_database(self, ctx: commands.Context) -> None:
        self.database.signup_collection.delete_many({})
        await ctx.send("data base cleared")

    @commands.command()
    @commands.has_role("Admin")
    async def close_signups(self, ctx: commands.Context):
        await ctx.message.delete()
        bingo_message = self.database.mgmt_collection.find_one(
            {"message_key": "signup message"}
        )

        if bingo_message.get("message id"):
            signup_message = await ctx.fetch_message(bingo_message.get("message id"))
            await discord.Message.delete(signup_message)
            self.database.mgmt_collection.delete_one(bingo_message)

            payment = self.database.mgmt_collection.find_one(
                {"message_key": "payment thread"}
            )
            payment_thread = await ctx.fetch_message(payment.get("message id"))
            await discord.Thread.delete(payment_thread)
            await discord.Message.delete(payment_thread)
            self.database.mgmt_collection.delete_one(payment)

            signup = self.database.mgmt_collection.find_one(
                {"message_key": "signup thread"}
            )
            signup_thread = await ctx.fetch_message(signup.get("message id"))
            await discord.Thread.delete(signup_thread)
            await discord.Message.delete(signup_thread)
            self.database.mgmt_collection.delete_one(signup)

            false = self.database.mgmt_collection.find_one(
                {"message_key": "false table"}
            )
            false_table_message = await ctx.fetch_message(false.get("message id"))
            await discord.Message.delete(false_table_message)
            self.database.mgmt_collection.delete_one(false)

            true = self.database.mgmt_collection.find_one({"message_key": "true table"})
            true_table_message = await ctx.fetch_message(true.get("message id"))
            await discord.Message.delete(true_table_message)
            self.database.mgmt_collection.delete_one(true)

            await ctx.send("Signups were closed")

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

        signup_message = await ctx.send(embed=embed, view=SignupView())
        await self.bot.database.add_persistent_message_id(
            "signup message", signup_message.id
        )

        signup_thread = await ctx.channel.send("All new signups go here")
        signup_notifications = await ctx.channel.create_thread(
            name="Signup Notifications", message=signup_thread
        )
        await self.bot.database.add_persistent_message_id(
            "signup thread", signup_notifications.id
        )

        paid_thread = await ctx.channel.send("Payment Notifications go here")
        payment_notifications = await ctx.channel.create_thread(
            name="Payment Notifications", message=paid_thread
        )
        await self.bot.database.add_persistent_message_id(
            "payment thread", payment_notifications.id
        )

        false_table, true_table = await build_signup_tables(self.database)

        false_table_message = await ctx.send(
            f"```ansi\n[2;31mUNPAID\n{false_table}[0m\n```"
        )
        await self.bot.database.add_persistent_message_id(
            "false table", false_table_message.id
        )
        true_table_message = await ctx.send(
            f"```ansi\n[2;36mPAID\n{true_table}[0m\n```"
        )
        await self.bot.database.add_persistent_message_id(
            "true table", true_table_message.id
        )

        await ctx.send("Signups are open")

    @commands.Cog.listener()
    async def on_ready(self):
        self.logger.info("signup cog loaded")


async def setup(bot):
    await bot.add_cog(Signup(bot))
