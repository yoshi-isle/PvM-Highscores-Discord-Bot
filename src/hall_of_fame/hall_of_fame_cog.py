import copy
import logging
import typing
import uuid
from datetime import datetime

import discord
from discord import app_commands
from discord.ext import commands

import constants.boss_info as boss_info
import constants.raid_names as raid_names
import hall_of_fame.constants.personal_best as personal_best
from constants.channels import ChannelIds
from constants.colors import Colors
from hall_of_fame import embed_generator
from hall_of_fame.time_helpers import convert_pb_to_display_format
from hall_of_fame.transformers import PbTimeTransformer

PENDING = "Pending "
APPROVED = "Approved "
FAILED = "Failed "
PB_SUBMISSION = "PB Submission"


class HallOfFame(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.logger = logging.getLogger("discord")
        self.database = self.bot.database

    @commands.command()
    async def raidpbs(self, ctx):
        channel = ctx.channel
        await channel.purge()
        data = await self.database.get_personal_bests()

        for info in raid_names.RAID_NAMES:
            await embed_generator.generate_boss_embed(
                ctx,
                data,
                info,
                pb_categories=raid_names.RAID_NAMES[info],
                number_of_placements=3,
            )

    @commands.command()
    async def bosspbs(self, ctx):
        channel = ctx.channel
        await channel.purge()
        data = await self.database.get_personal_bests()

        for groups in boss_info.BOSS_INFO:
            embeds = []
            for boss in groups:
                embeds.append(
                    await embed_generator.generate_boss_embed(
                        ctx, data, boss["boss_name"], number_of_placements=3
                    )
                )
            await ctx.send(embeds=embeds)

    async def submit_boss_pb_autocomplete(
        self,
        interaction: discord.Interaction,
        current: str,
    ) -> typing.List[app_commands.Choice[str]]:
        data = []

        return [
            app_commands.Choice(name=boss["boss_name"], value=boss["boss_name"])
            for category in boss_info.BOSS_INFO
            for boss in category
            if current.lower() in boss["boss_name"].lower()
        ]

    @app_commands.command(name="submit_boss_pb")
    @app_commands.describe(boss_name="Submit a boss PB")
    @app_commands.autocomplete(boss_name=submit_boss_pb_autocomplete)
    async def submit_boss_pb(
        self,
        interaction: discord.Interaction,
        pb: PbTimeTransformer,
        boss_name: str,
        osrs_username: str,
        image: discord.Attachment,
    ):
        self.logger.info("Running submit_boss_pb command")

        approve_channel = self.bot.get_channel(ChannelIds.approve_channel)
        self.logger.info("Got approved channel")

        # TODO: Turn this back on
        # if image is None:
        #     await interaction.response.send_message("Please upload an image.")
        #     return

        # TODO: check if boss is equal to one in the submit_boss_pb_autocomplete list (spelled correctly. case-sensitive)

        description = f"@{interaction.user.display_name} is submitting a PB of: {await convert_pb_to_display_format(pb)} for **{boss_name}**!\n\nClick the '👍' to approve."
        self.logger.info("Built the submission embed description")
        time_of_submission = datetime.now()
        self.logger.info("Building PersonalBest model")
        # Build the PersonalBest model and insert a record
        formatted_personal_best = personal_best.PersonalBest(
            id=uuid.uuid4(),
            boss=boss_name,
            pb=pb,
            approved=False,
            date_achieved=time_of_submission,
            discord_cdn_url=image.url,
            osrs_username=osrs_username,
            discord_username=interaction.user.display_name,
        )
        self.logger.info(
            "Attempting to insert the PersonalBest into DB with approved: False"
        )
        id = await self.database.insert_personal_best_submission(
            formatted_personal_best
        )
        self.logger.info(f"Success! adding record ID '{id}' to embed footer")

        embed = await embed_generator.generate_pb_submission_embed(
            title=PENDING + PB_SUBMISSION,
            description=description,
            color=Colors.yellow,
            timestamp=time_of_submission,
            image_url=image.url,
            footer_id=id,
        )
        self.logger.info(f"Sending embed to the appropriate approval channel")

        message = await approve_channel.send(embed=embed)
        emojis = [
            "👍",
            "👎",
        ]

        self.logger.info(f"Adding reaction emojis to embed")

        for emoji in emojis:
            await message.add_reaction(emoji)

        self.logger.info(f"Sending pending ephemeral message to user")

        await interaction.response.send_message(
            "Submission is pending!", ephemeral=True
        )

    async def submit_raid_pb_autocomplete(
        self,
        interaction: discord.Interaction,
        current: str,
    ) -> typing.List[app_commands.Choice[str]]:
        data = []
        for raid_name in raid_names.RAID_NAMES:
            if current.lower() in raid_name.lower():
                data.append(app_commands.Choice(name=raid_name, value=raid_name))
        return data

    @app_commands.command(name="submit_raid_pb")
    @app_commands.describe(raid_name="Submit a raid PB")
    @app_commands.autocomplete(raid_name=submit_raid_pb_autocomplete)
    async def submit_raid_pb(
        self,
        interaction: discord.Interaction,
        pb: PbTimeTransformer,
        raid_name: str,
        group_size: int,
        osrs_usernames: str,
        image: discord.Attachment,
    ):
        approve_channel = self.bot.get_channel(ChannelIds.approve_channel)

        if image is None:
            await interaction.response.send_message("Please upload an image.")
            return

        result = [osrs_usernames.strip() for x in osrs_usernames.split(",")]

        if len(result) != group_size:
            await interaction.response.send_message(
                f"**Error -** the group size does not match the number of names given.\nExpected **{group_size}** name(s) and only received **{len(result)}**.\nYou entered: **'{osrs_usernames}**.'\nPlease try again and provide your raid group in the following format: **'Player1, Player2, Player 3'**"
            )
            return

        # TODO: check if boss is equal to one in the submit_boss_pb_autocomplete list (spelled correctly. case-sensitive)
        # TODO: valid string checker for group size
        # TODO: Neat looking osrs_usernames string. Example "Person1, Person2, Person3" -> "Person 1, Person2, and Person 3"
        description = f"Raid name: **{raid_name}**\nTeam members: **{osrs_usernames}**\nGroup size: **{group_size}**\nPB: **{await convert_pb_to_display_format(pb)}**\n\nClick the '👍' to approve.\n\nDouble check carefully to make sure the group size matches up."

        time_of_submission = datetime.now()

        # Build the PersonalBest model and insert a record
        formatted_personal_best = personal_best.PersonalBest(
            id=uuid.uuid4(),
            boss=raid_name,
            pb=pb,
            approved=False,
            date_achieved=time_of_submission,
            discord_cdn_url=image.url,
            osrs_username=osrs_usernames,
            discord_username=interaction.user.display_name,
        )
        id = await self.database.insert_personal_best_submission(
            formatted_personal_best
        )

        embed = await embed_generator.generate_pb_submission_embed(
            title=PENDING + PB_SUBMISSION,
            description=description,
            color=Colors.yellow,
            timestamp=time_of_submission,
            image_url=image.url,
            footer_id=id,
        )

        message = await approve_channel.send(embed=embed)
        await message.add_reaction("👍")
        await message.add_reaction("👎")

        await interaction.response.send_message(
            "Submission is pending!", ephemeral=True
        )

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
                    new_prefix = ""
                    new_color = ""

                    # approved submission
                    if payload.emoji.name == "👍":
                        await channel.send(
                            f"{payload.member.display_name} approved submission! 👍",
                            reference=message,
                        )
                        # TODO: probably try-catch the embed.footer.text instead of just shoving into an insert
                        await self.database.update_personal_best_approval(
                            embed.footer.text, True
                        )
                        new_prefix = APPROVED
                        new_color = Colors.green

                    # not approved submission
                    elif payload.emoji.name == "👎":
                        await channel.send(
                            f"{payload.member.display_name} denied the submission 👎",
                            reference=message,
                        )
                        new_prefix = FAILED
                        new_color = Colors.red

                    # deep copy so that we can update the embed
                    new_embed = copy.deepcopy(embed)
                    new_embed.title = new_prefix + PB_SUBMISSION
                    new_embed.color = new_color
                    await message.edit(embed=new_embed)
                    await message.clear_reactions()

                    # Now update the highscores...
                    # TODO - Too much complexity going on
                    # TODO - what type of PB is it?
                    # grab the messages in the boss highscores
                    highscorechannel = self.bot.get_channel(ChannelIds.boss_pbs)

                    messages = [
                        message
                        async for message in highscorechannel.history(
                            limit=200, oldest_first=True
                        )
                    ]

                    # Update categories of PBs
                    data = await self.database.get_personal_bests()

                    # TODO - the assumption is that the ratio of messages
                    # in the channel is 1:1 with the number of categories of boss info
                    # need checks in place for this
                    for m in range(len(messages)):
                        # At this point, we're inside the a message and are
                        # pointing at the same index of 'boss info'

                        # the 'edited embeds' to post
                        newembeds = []

                        # this is every boss in the sliced category
                        for boss in boss_info.BOSS_INFO[m]:
                            newembeds.append(
                                await embed_generator.generate_boss_embed(
                                    channel,
                                    data,
                                    boss["boss_name"],
                                    number_of_placements=3,
                                )
                            )
                        await messages[m].edit(embeds=newembeds)

    async def cog_app_command_error(
        self, interaction: discord.Interaction, error: app_commands.AppCommandError
    ):
        if isinstance(error, discord.app_commands.TransformerError):
            error_message = f"The following time of **{error.value}** did not conform to the time format. It needs to be in 00:00.00 format"
            await interaction.response.send_message(f"{error_message}", ephemeral=True)

    @commands.Cog.listener()
    async def on_ready(self):
        self.logger.info("hof cog loaded")


async def setup(bot):
    await bot.add_cog(HallOfFame(bot))
