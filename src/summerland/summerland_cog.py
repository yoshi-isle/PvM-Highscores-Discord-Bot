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
from PIL import Image
from discord import Embed
from constants.colors import Colors
import time


class Summerland(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.logger = logging.getLogger("discord")
        self.database = self.bot.database

    @commands.Cog.listener()
    async def on_ready(self):
        self.logger.info("summerland cog loaded")

    @app_commands.command(name="team_info")
    async def team_info(
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

        await interaction.response.send_message()
        embed = await embed_generator.generate_team_embed(record)

    @commands.command()
    async def force_update_current_standings(
        self,
        ctx: commands.Context,
    ) -> None:
        await self.update_standings()

    @app_commands.command(name="submit")
    @app_commands.describe(
        image="Submit an image for your tile (partial completion is ok)"
    )
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
        """
        This is a check for every reaction that happens
        """
        # ignore the reactions from the bot
        member = payload.member
        if member.bot:
            return

        # only check the reactions on the approve channel
        channel = self.bot.get_channel(payload.channel_id)
        if channel.id == ChannelIds.approve_channel:
            # grab the actual message the reaction was too
            message = await channel.fetch_message(payload.message_id)

            # the message must contain an embed
            if message.embeds:
                embed = message.embeds[0]

                # We only want to edit pending submissions
                if "Pending" in embed.title:

                    # Approved submission
                    if payload.emoji.name == "👍":
                        time.sleep(20)
                        guid = embed.footer.text

                        # Find the embed in the team channel that has the guid
                        team_info = await self.find_team_channel_by_submission_guid(
                            guid
                        )
                        team_channel = self.bot.get_channel(
                            int(team_info[0]["channel_id"])
                        )

                        await channel.send(
                            f"<@{payload.member.id}> approved the submission for {team_channel.mention}! 👍",
                            reference=message,
                        )

                        new_embed = embed
                        new_embed.title = "[APPROVED]"
                        new_embed.color = Colors.green
                        new_embed.remove_footer()
                        await message.edit(embed=new_embed)
                        await message.clear_reactions()

                        if team_channel is not None:
                            pending_submission_message = [
                                message
                                async for message in team_channel.history(
                                    limit=200, oldest_first=True
                                )
                                if len(message.embeds) != 0
                                and message.embeds[0].footer.text == guid
                            ]
                            approved_submission_message = pending_submission_message[0]
                            approved_submission_embed = (
                                approved_submission_message.embeds[0]
                            )
                            approved_submission_embed.color = Colors.green
                            approved_submission_embed.title = "[Approved]"
                            approved_submission_embed.remove_field(1)
                            approved_submission_embed.remove_footer()
                            await approved_submission_message.edit(
                                embed=approved_submission_embed
                            )

                            # Remove the guid from pending submissions field in db record
                            team_info = await self.database.get_team_info(
                                team_channel.id
                            )
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
                                team_info, team_channel, approved_submission_message
                            )

    async def get_top_teams(self, data):
        """
        Sorts the top teams from the team informations given
        """
        all_teams = (result for result in data)
        return sorted(all_teams, key=operator.itemgetter("current_tile"), reverse=True)

    async def generate_current_standings_text(self, teams):
        current_standings_text = ""
        current_placement = 1
        for i in range(len(teams)):
            current_standings_text += f"> **{PLACEMENT_EMOJIS.get(current_placement)}{teams[i]['team_name']} - **Tile {teams[i]['current_tile']}: {BINGO_TILES[teams[i]['current_tile']]['Name']}\n"
            if i < len(teams) - 1:
                if teams[i]["current_tile"] > teams[i + 1]["current_tile"]:
                    current_placement = current_placement + 1

        return current_standings_text

    async def find_team_channel_by_submission_guid(self, guid):
        all_teams = await self.database.get_all_teams()
        return [team for team in all_teams if guid in team["pending_submissions"]]

    async def attempt_to_progress(
        self, team_info, team_channel, pending_submission_message
    ):
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
                embed = Embed(
                    title=f"✅ Submission Approved. Your team is now at **{increment_progress}** out of **{submissions_needed}** for the tile.",
                )
                await team_channel.send(
                    embed=embed, reference=pending_submission_message
                )
                return increment_progress

        # Roll
        roll = random.randint(1, 4)
        new_tile = int(team_info["current_tile"]) + int(roll)
        # Progress counter back to 0
        await self.database.update_team_tile(
            team_info["channel_id"], "progress_counter", 0
        )

        await self.database.update_team_tile(
            team_info["channel_id"], "current_tile", new_tile
        )

        embed = Embed(
            title=f"✅ Submission Approved.",
        )
        await team_channel.send(embed=embed, reference=pending_submission_message)

        # Roll dice, send roll embed, update team tile, reset progress counter
        await team_channel.send(
            embed=await embed_generator.generate_dice_roll_embed(roll)
        )
        record = await self.database.get_team_info(team_channel.id)

        await team_channel.send(
            embed=await embed_generator.generate_new_tile_embed(record)
        )

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


async def setup(bot):
    await bot.add_cog(Summerland(bot))
