import logging
import operator
import discord
import uuid
import summerland.embed_generator as embed_generator
from Crypto.Random import random
from discord import app_commands
from discord.ext import commands
from summerland.constants.channels import ChannelIds
from summerland.constants.tiles import BINGO_TILES
from summerland.constants.board_piece_images import BOARD_PIECE_IMAGES
from summerland.constants.placement_emojis import PLACEMENT_EMOJIS
from summerland.constants.team_icon_emojis import TEAM_ICON_EMOJIS

from PIL import Image
from discord import Embed
from constants.colors import Colors
from datetime import datetime, timedelta
import time


class Summerland(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.logger = logging.getLogger("discord")
        self.database = self.bot.database
        self.cooldown = 20
        self.last_used = 0

    @commands.Cog.listener()
    async def on_ready(self):
        self.logger.info("summerland cog loaded")

    @app_commands.command(name="team_info")
    @commands.has_role("Summerland 2024")
    async def team_info(
        self,
        interaction: discord.Interaction,
    ) -> None:
        # Get the ID of the channel we're in
        # Make sure it's in the DB
        record = await self.database.get_team_info(interaction.channel.id)
        if record is None:
            await interaction.response.send_message(
                "Sorry. Can't find info for this team."
            )
            return
        current_placement = await self.get_team_placement(interaction.channel.id)

        await interaction.response.send_message(
            embed=await embed_generator.generate_team_embed(record, current_placement),
        )

    @app_commands.command(name="reroll")
    @commands.has_role("Summerland 2024")
    async def reroll(
        self,
        interaction: discord.Interaction,
    ) -> None:
        # Get the ID of the channel we're in
        this_channel_id = interaction.channel.id
        # Make sure it's in the DB
        record = await self.database.get_team_info(this_channel_id)
        if record is None:
            await interaction.response.send_message(
                "Sorry. Can't find info for this team."
            )
            return
        # Cool looking discord timestamp
        twelve_hours_from_now = record["last_reroll"] + timedelta(hours=12)
        epoch = round(twelve_hours_from_now.timestamp())
        disc_dt = f"<t:{epoch}:R>"
        if datetime.now() < twelve_hours_from_now:
            await interaction.response.send_message(
                f"You are not eligible for a reroll until {disc_dt}"
            )
            return

        current_placement = await self.get_team_placement(interaction.channel.id)
        if current_placement == 1:
            await interaction.response.send_message(
                f"You are not eligible for a reroll since your team is in 1st place"
            )
            return

        await interaction.response.send_message(
            f"# {interaction.user.mention} is re-rolling for the team"
        )
        await self.reroll_tile(record, interaction.channel)

    @commands.command()
    async def drawsomething3452345(
        self,
        ctx: commands.Context,
    ) -> None:
        await ctx.send(embed=await embed_generator.test())

    @commands.command()
    @commands.has_role("Admin")
    async def force_update_current_standings(
        self,
        ctx: commands.Context,
    ) -> None:
        await self.update_standings()

    @commands.command()
    @commands.has_role("Admin")
    async def initial_roll(
        self,
        ctx: commands.Context,
    ) -> None:
        this_channel_id = ctx.channel.id
        # Make sure it's in the DB
        record = await self.database.get_team_info(this_channel_id)
        if record is None:
            await ctx.response.send_message("Sorry. Can't find info for this team.")
            return
        await self.initial_progress(record, ctx.channel)
        await self.update_standings()

    @app_commands.command(name="submit")
    @app_commands.describe(
        image="Submit an image for your tile (partial completion is ok)"
    )
    @app_commands.checks.has_role("Summerland 2024")
    async def submit(
        self,
        interaction: discord.Interaction,
        image: discord.Attachment,
    ):
        this_channel_id = interaction.channel.id
        team_info = await self.database.get_team_info(this_channel_id)
        guid = str(uuid.uuid4())
        approve_channel = self.bot.get_channel(ChannelIds.approve_channel)
        is_partial = BINGO_TILES[team_info["current_tile"]]["CompletionCounter"] > 1
        # Keeps track of pending submission uuid for front-end stuff
        pending_submissions = team_info["pending_submissions"]
        if pending_submissions is None:
            pending_submissions = []
        pending_submissions.append(guid)
        await self.database.update_team_tile(
            str(this_channel_id), "pending_submissions", pending_submissions
        )

        # Submission receipt for the team's channel
        await interaction.response.send_message(
            embed=await embed_generator.generate_submission_receipt_embed(
                guid, image.url, interaction, BINGO_TILES[team_info["current_tile"]]
            )
        )

        # Approval embed for admins
        message = await approve_channel.send(
            embed=await embed_generator.generate_admin_approval_embed(
                guid,
                image.url,
                interaction,
                team_info,
                BINGO_TILES[team_info["current_tile"]],
                is_partial,
            )
        )

        await message.add_reaction("👍")
        await message.add_reaction("👎")
        if is_partial:
            await message.add_reaction("🎲")

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        # Ignore the reactions from the bot
        member = payload.member
        if member.bot:
            return

        # Only check the reactions on the approve channel
        channel = self.bot.get_channel(payload.channel_id)
        if channel.id != ChannelIds.approve_channel:
            return

        # Grab the message and embed
        message = await channel.fetch_message(payload.message_id)
        embed = message.embeds[0]

        # The message must contain an embed
        if not message.embeds:
            return

        # We only want to edit pending submissions
        if "Pending" not in embed.title:
            return

        # Eager beaver check
        if time.time() < self.last_used + self.cooldown:
            await channel.send(
                f"Woahoho there eager beaver. please wait {round((self.last_used + self.cooldown) - time.time())} seconds",
                reference=message,
            ),
            return

        # Variables
        self.last_used = time.time()
        guid = embed.footer.text

        # Find the embed in the team channel that has the guid
        team_info = await self.find_team_channel_by_submission_guid(guid)
        if len(team_info) == 0:
            await channel.send(
                f"That submission doesn't exist anymore or is outdated.",
                reference=message,
            )
            return
        team_channel = self.bot.get_channel(int(team_info[0]["channel_id"]))

        if payload.emoji.name == "👍":
            # Admin approval receipt
            await channel.send(
                f"<@{payload.member.id}> approved the submission for {team_channel.mention}! 👍",
                reference=message,
            )
            await self.send_admin_notification(
                f"{payload.member.name} approved a submission for {team_channel.mention}"
            )

            await message.edit(
                embed=await embed_generator.update_admin_approved_embed(embed)
            )

            await message.clear_reactions()

            team_submission_message = [
                message
                async for message in team_channel.history(limit=200, oldest_first=False)
                if len(message.embeds) != 0 and message.embeds[0].footer.text == guid
            ][0]

            await team_submission_message.edit(
                embed=await embed_generator.update_channel_approved_embed(
                    team_submission_message.embeds[0]
                )
            )

            # Remove the guid from pending submissions field in db record
            team_info = await self.database.get_team_info(team_channel.id)
            pending_submissions_list = team_info["pending_submissions"]
            pending_submissions_list.remove(guid)
            if pending_submissions_list is None:
                pending_submissions_list = []
            await self.database.update_team_tile(
                str(team_channel.id),
                "pending_submissions",
                pending_submissions_list,
            )

            # Roll or update progress
            await self.attempt_to_progress(
                team_info,
                team_channel,
                team_submission_message,
                False,
                embed.image,
            )
        if payload.emoji.name == "👎":
            # Admin approval receipt
            await channel.send(
                f"<@{payload.member.id}> denied the submission for {team_channel.mention} 👎 (Please let them know why)",
                reference=message,
            )

            await self.send_admin_notification(
                f"{payload.member.name} denied a submission for {team_channel.mention}"
            )

            await message.edit(
                embed=await embed_generator.update_admin_denied_embed(embed)
            )

            await message.clear_reactions()

            team_submission_message = [
                message
                async for message in team_channel.history(limit=200, oldest_first=False)
                if len(message.embeds) != 0 and message.embeds[0].footer.text == guid
            ][0]

            await team_submission_message.edit(
                embed=await embed_generator.update_denied_approved_embed(
                    team_submission_message.embeds[0]
                )
            )

            # Remove the guid from pending submissions field in db record
            team_info = await self.database.get_team_info(team_channel.id)
            pending_submissions_list = team_info["pending_submissions"]
            pending_submissions_list.remove(guid)
            if pending_submissions_list is None:
                pending_submissions_list = []
            await self.database.update_team_tile(
                str(team_channel.id),
                "pending_submissions",
                pending_submissions_list,
            )

            # Send the submission denied notification
            embed = Embed(
                title=f"❌ Submission Denied. A bingo admin will be in touch soon",
            )
            await team_channel.send(embed=embed, reference=team_submission_message)

        if payload.emoji.name == "🎲":
            # Admin approval receipt
            await channel.send(
                f"<@{payload.member.id}> force completed the submission for {team_channel.mention}! 🎲",
                reference=message,
            )

            await self.send_admin_notification(
                f"{payload.member.name} force-completed a submission for {team_channel.mention}"
            )

            await message.edit(
                embed=await embed_generator.update_admin_approved_embed(embed)
            )

            await message.clear_reactions()

            team_submission_message = [
                message
                async for message in team_channel.history(limit=200, oldest_first=False)
                if len(message.embeds) != 0 and message.embeds[0].footer.text == guid
            ][0]

            await team_submission_message.edit(
                embed=await embed_generator.update_channel_approved_embed(
                    team_submission_message.embeds[0]
                )
            )

            # Remove the guid from pending submissions field in db record
            team_info = await self.database.get_team_info(team_channel.id)
            pending_submissions_list = team_info["pending_submissions"]
            pending_submissions_list.remove(guid)
            if pending_submissions_list is None:
                pending_submissions_list = []
            await self.database.update_team_tile(
                str(team_channel.id),
                "pending_submissions",
                pending_submissions_list,
            )

            # Roll or update progress
            await self.attempt_to_progress(
                team_info,
                team_channel,
                team_submission_message,
                True,
                embed.image,
            )

    async def get_top_teams(self, data):
        """
        Sorts the top teams from the team informations given
        """
        all_teams = (result for result in data)
        return sorted(all_teams, key=operator.itemgetter("current_tile"), reverse=True)

    async def get_team_placement(self, channel_id):
        """
        Sorts the top teams from the team informations given
        """
        all_teams = await self.database.get_all_teams()
        all_teams = (result for result in all_teams)
        top_teams = sorted(
            all_teams, key=operator.itemgetter("current_tile"), reverse=True
        )

        current_placement = 1
        for i in range(len(top_teams)):
            if i < len(top_teams) - 1:
                if top_teams[i]["channel_id"] == str(channel_id):
                    return current_placement
                if top_teams[i]["current_tile"] > top_teams[i + 1]["current_tile"]:
                    current_placement = current_placement + 1
        return current_placement

    async def generate_current_standings_text(self, teams):
        current_standings_text = ""
        current_placement = 1
        for i in range(len(teams)):
            if teams[i]["win"] == True:
                current_standings_text += (
                    f"Team {teams[i]['team_name']} won the game!\n\n"
                )
            current_standings_text += f"> **{PLACEMENT_EMOJIS.get(current_placement)}{teams[i]['team_name']} {TEAM_ICON_EMOJIS[teams[i]['team_number']]} - **Tile {teams[i]['current_tile']}: {BINGO_TILES[teams[i]['current_tile']]['Name']}\n"
            if i < len(teams) - 1:
                if teams[i]["current_tile"] > teams[i + 1]["current_tile"]:
                    current_placement = current_placement + 1

        return current_standings_text

    async def find_team_channel_by_submission_guid(self, guid):
        all_teams = await self.database.get_all_teams()
        return [team for team in all_teams if guid in team["pending_submissions"]]

    async def reroll_tile(self, team_info, team_channel):
        tile_history = team_info["tile_history"]
        last_tile = 0
        if len(tile_history) < 2:
            last_tile = 0
        else:
            last_tile = tile_history[len(tile_history) - 2]

        roll = 0
        while True:
            roll = random.randint(1, 4)
            if roll is not int(team_info["current_tile"] - last_tile):
                break

        new_tile = last_tile + roll

        await self.send_admin_notification(
            f"{team_info['team_name']} is re-rolling, rolling a {roll} and putting them on {new_tile}. ({BINGO_TILES[new_tile]['Name']})"
        )

        await self.database.update_team_tile(
            team_info["channel_id"], "current_tile", new_tile
        )

        await self.database.update_team_tile(
            team_info["channel_id"], "last_reroll", datetime.now()
        )

        await team_channel.send(
            embed=await embed_generator.generate_dice_roll_embed(roll)
        )

        tile_history = team_info["tile_history"]
        tile_history = tile_history[:-1]
        tile_history.append(new_tile)

        await self.database.update_team_tile(
            team_info["channel_id"],
            "tile_history",
            tile_history,
        )

        record = await self.database.get_team_info(team_info["channel_id"])

        await team_channel.send(
            embed=await embed_generator.generate_rerolled_tile_embed(record)
        )

        await self.update_standings()

    async def initial_progress(self, team_info, team_channel):
        # Roll
        roll = random.randint(1, 4)
        await self.database.update_team_tile(
            team_info["channel_id"], "current_tile", roll
        )

        await self.send_admin_notification(
            f"{team_info['team_name']} is starting their initial roll, rolling a {roll}. ({BINGO_TILES[roll]['Name']})"
        )

        tile_history = team_info["tile_history"]
        tile_history.append(roll)

        await self.database.update_team_tile(
            team_info["channel_id"], "last_reroll", datetime.now()
        )

        await self.database.update_team_tile(
            team_info["channel_id"],
            "tile_history",
            tile_history,
        )

        # Roll dice, send roll embed, update team tile, reset progress counter
        await team_channel.send(
            embed=await embed_generator.generate_dice_roll_embed(roll)
        )
        record = await self.database.get_team_info(team_channel.id)

        await team_channel.send(
            embed=await embed_generator.generate_new_tile_embed(record)
        )

        await self.update_standings()

    async def attempt_to_progress(
        self,
        team_info,
        team_channel,
        pending_submission_message,
        force,
        completed_image,
    ):
        embed = Embed(
            title=f"✅ Submission Approved.",
        )
        old_tile = team_info["current_tile"]
        await team_channel.send(embed=embed, reference=pending_submission_message)

        if not force:
            # Partial tile?
            tile = BINGO_TILES[team_info["current_tile"]]
            submissions_needed = tile["CompletionCounter"]
            is_partial = submissions_needed > 1

            # If it's a partial tile, update the counter.
            # If the counter turns out to be >= than the completion counter, we can roll
            if is_partial:
                increment_progress = team_info["progress_counter"] + 1
                await self.database.update_team_tile(
                    team_info["channel_id"], "progress_counter", increment_progress
                )
                if increment_progress < tile["CompletionCounter"]:
                    await self.send_admin_notification(
                        f"{team_info['team_name']} progressed on their tile, and is now **{increment_progress}** out of **{submissions_needed}** ({BINGO_TILES[team_info['current_tile']]['Name']})"
                    )
                    embed = Embed(
                        title=f"✅ Submission Approved. Your team is now at **{increment_progress}** out of **{submissions_needed}** for the tile.",
                    )
                    await team_channel.send(
                        embed=embed, reference=pending_submission_message
                    )
                    return increment_progress

        # Did they win
        if team_info["current_tile"] == 100:
            await self.send_admin_notification(
                f"{team_info['team_name']} won the game."
            )
            await self.team_wins(team_info, team_channel)
            return

        # Roll
        roll = random.randint(1, 4)

        new_tile = int(team_info["current_tile"]) + int(roll)
        if new_tile > 100:
            new_tile = 100

        await self.send_admin_notification(
            f"{team_info['team_name']} fully completed their tile, rolling a {roll} and putting them on {new_tile}. ({BINGO_TILES[new_tile]['Name']})"
        )
        # Roll dice embed
        await team_channel.send(
            embed=await embed_generator.generate_dice_roll_embed(roll)
        )
        record = await self.database.get_team_info(team_channel.id)

        if new_tile == 10:
            await team_channel.send(
                embed=await embed_generator.generate_setback_or_skip_embed(
                    new_tile,
                    "You landed on a setback tile...",
                    "You think I just made these for fun?!?! Go back to tile 4!",
                )
            )

            new_tile = 4

            await self.send_admin_notification(
                f"{team_info['team_name']} landed on a set-back tile, putting them back to {new_tile}. ({BINGO_TILES[new_tile]['Name']})"
            )

            # Just double add the tile to tile_history to signify setback
            tile_history = team_info["tile_history"]
            tile_history.append(new_tile)

            await self.database.update_team_tile(
                team_info["channel_id"],
                "tile_history",
                tile_history,
            )

        if new_tile == 17:
            await team_channel.send(
                embed=await embed_generator.generate_setback_or_skip_embed(
                    new_tile,
                    "You landed on a skip tile!",
                    "Ride the Quetzin to tile 23!",
                )
            )

            new_tile = 23

            await self.send_admin_notification(
                f"{team_info['team_name']} landed on a skip-forward tile, skipping them to {new_tile}. ({BINGO_TILES[new_tile]['Name']})"
            )

        if new_tile == 40:
            await team_channel.send(
                embed=await embed_generator.generate_setback_or_skip_embed(
                    new_tile,
                    "You landed on a skip tile!",
                    "Take the fairy ring to tile 47!",
                )
            )

            new_tile = 47

            await self.send_admin_notification(
                f"{team_info['team_name']} landed on a skip-forward tile, skipping them to {new_tile}. ({BINGO_TILES[new_tile]['Name']})"
            )

        if new_tile == 63:
            await team_channel.send(
                embed=await embed_generator.generate_setback_or_skip_embed(
                    new_tile,
                    "You landed on a skip tile!",
                    "An enlightned journey! Take the hot air balloon to tile 69!",
                )
            )

            new_tile = 69

            await self.send_admin_notification(
                f"{team_info['team_name']} landed on a skip-forward tile, skipping them to {new_tile}. ({BINGO_TILES[new_tile]['Name']})"
            )

        if new_tile == 79:
            await team_channel.send(
                embed=await embed_generator.generate_setback_or_skip_embed(
                    new_tile,
                    "You landed on a setback tile...",
                    "Disconnected and died... back to tile 73",
                )
            )

            new_tile = 73

            await self.send_admin_notification(
                f"{team_info['team_name']} landed on a set-back tile, putting them back to {new_tile}. ({BINGO_TILES[new_tile]['Name']})"
            )

            # Just double add the tile to tile_history to signify setback
            tile_history = team_info["tile_history"]
            tile_history.append(new_tile)

            await self.database.update_team_tile(
                team_info["channel_id"],
                "tile_history",
                tile_history,
            )

        # Progress counter back to 0
        await self.database.update_team_tile(
            team_info["channel_id"], "progress_counter", 0
        )

        await self.database.update_team_tile(
            team_info["channel_id"], "current_tile", new_tile
        )

        await self.database.update_team_tile(
            team_info["channel_id"], "pending_submissions", []
        )

        await self.database.update_team_tile(
            team_info["channel_id"], "last_reroll", datetime.now()
        )

        tile_history = team_info["tile_history"]
        tile_history.append(new_tile)

        await self.database.update_team_tile(
            team_info["channel_id"],
            "tile_history",
            tile_history,
        )

        record = await self.database.get_team_info(team_channel.id)

        await team_channel.send(
            embed=await embed_generator.generate_new_tile_embed(record)
        )

        changelog_channel = self.bot.get_channel(ChannelIds.changelog)

        tile_completed_embed = Embed(
            title="",
            description=f"**{team_info['team_name']}** completed: {BINGO_TILES[old_tile]['Name']}\n🎲 Rolled a **{roll}**.\n**Now on tile:** {record['current_tile']} - {BINGO_TILES[record['current_tile']]['Name']}\nhttps://discord.com/channels/1197595466657968158/1237804690570481715",
        )
        tile_completed_embed.color = Colors.green
        tile_completed_embed.set_thumbnail(url=team_info["team_image"])

        tile_completed_embed.set_image(url=completed_image.url)
        await changelog_channel.send(embed=tile_completed_embed)

        await self.update_standings()

    async def update_standings(self):
        teams = await self.database.get_all_teams()
        teams = await self.get_top_teams(teams)
        current_standings_channel = self.bot.get_channel(ChannelIds.current_standings)
        await current_standings_channel.purge()

        # Generate board image
        with Image.open("src/summerland/images/board_dimmed.png") as img:
            for record in teams:
                with Image.open(
                    BOARD_PIECE_IMAGES.get(record["team_number"])
                ) as team_board_piece_img:
                    team_board_piece_img = team_board_piece_img.convert("RGBA")
                    position = BINGO_TILES[record["current_tile"]]["PieceCoordinate"]
                    img.paste(team_board_piece_img, position, team_board_piece_img)

            img.save("final_board.png")
            final_board_image = discord.File("final_board.png")
            await current_standings_channel.send(file=final_board_image)

        # Generate embed for top teams
        embed_field_text = await self.generate_current_standings_text(teams)
        await current_standings_channel.send(
            embed=await embed_generator.generate_top_teams_embed(embed_field_text)
        )

    async def send_admin_notification(self, text):
        admin_notifications_channel = self.bot.get_channel(
            ChannelIds.admin_notifications
        )

        await admin_notifications_channel.send(f"```{text}```")

    async def team_wins(self, team_info, team_channel):
        await self.database.update_team_tile(team_info["channel_id"], "win", True)
        await team_channel.send("# Congratulations! Your team finished the board!! 🎉")


async def setup(bot):
    await bot.add_cog(Summerland(bot))
