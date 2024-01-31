import copy
import logging
import typing
import uuid
from datetime import datetime

import discord
from discord import app_commands
from discord.ext import commands

import constants.raid_names as raid_names
import constants.forum_data as forum_data
import hall_of_fame.constants.personal_best as personal_best
from constants.channels import ChannelIds
from constants.colors import Colors
from hall_of_fame import embed_generator
from hall_of_fame.services import highscores_service
from hall_of_fame.time_helpers import convert_pb_to_display_format
from hall_of_fame.transformers import PbTimeTransformer
from hall_of_fame.autocompletes.autocompletes import AutoComplete
import hall_of_fame.data_helper as data_helper
import constants.forum_data.theatre_of_blood as theatre_of_blood
import constants.forum_data.theatre_of_blood as theatre_of_blood
import constants.forum_data.chambers_of_xeric as chambers_of_xeric
import constants.forum_data.tombs_of_amascut as tombs_of_amascut
import constants.forum_data.tzhaar as tzhaar
import constants.forum_data.dt2bosses as dt2bosses
import constants.forum_data.bosses as bosses
import constants.forum_data.misc_activities as misc_activities

PENDING = "Pending "
APPROVED = "Approved "
FAILED = "Failed "
PB_SUBMISSION = "PB Submission"


class HallOfFame(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.logger = logging.getLogger("discord")
        self.database = self.bot.database
        self.approve_channel = self.bot.get_channel(ChannelIds.approve_channel)

    group = app_commands.Group(
        name="submit",
        description="Submit a PB",
    )

    # Sub-command to submit TOB PBs
    @group.command(name="tob")
    async def theatre_of_blood(
        self,
        interaction: discord.Interaction,
        mode: AutoComplete.TOB_MODES,
        group_size: AutoComplete.TOB_GROUPSIZES,
        group_members: str,
        time: PbTimeTransformer,
        image: discord.Attachment,
    ) -> None:
        approve_channel = self.bot.get_channel(ChannelIds.approve_channel)
        size = int(group_size.name)

        if not data_helper.is_valid_group_members_string(group_members, size):
            await interaction.response.send_message(
                f"Group members doesn't match the number of names given for group size of **{size}**.\nYou entered: **'{group_members}**.\nPlease try again with your raid group in the following format: **'Player1, Player2, Player 3...'**",
                ephemeral=True,
            )
            return

        raid_name = data_helper.get_tob_raid_name(size, mode)
        time_of_submission = datetime.now()
        formatted_personal_best = personal_best.PersonalBest(
            id=uuid.uuid4(),
            boss=raid_name,
            pb=time,
            approved=False,
            date_achieved=time_of_submission,
            discord_cdn_url=image.url,
            osrs_username=group_members,
            discord_username=interaction.user.display_name,
        )
        id = await self.database.insert_personal_best_submission(
            formatted_personal_best
        )

        embed = await embed_generator.generate_pb_submission_embed(
            title=PENDING + PB_SUBMISSION,
            description=f"Raid name: **{raid_name}**\nTeam Members: **{group_members}**\nTime: **{await convert_pb_to_display_format(time)}**\n",
            color=Colors.yellow,
            timestamp=time_of_submission,
            image_url=image.url,
            footer_id=id,
        )
        message = await approve_channel.send(embed=embed)
        await message.add_reaction("👍")
        await message.add_reaction("👎")
        await interaction.response.send_message(
            "Thank you for your submission. Please wait for an admin to approve :)",
            ephemeral=True,
        )

    # Sub-command to submit COX PBs
    @group.command(name="cox")
    async def chambers_of_xeric(
        self,
        interaction: discord.Interaction,
        mode: AutoComplete.COX_MODES,
        group_size: AutoComplete.COX_GROUPSIZES,
        group_members: str,
        time: PbTimeTransformer,
        image: discord.Attachment,
    ) -> None:
        approve_channel = self.bot.get_channel(ChannelIds.approve_channel)
        size = int(group_size.name)

        if not data_helper.is_valid_group_members_string(group_members, size):
            await interaction.response.send_message(
                f"Group members doesn't match the number of names given for group size of **{size}**.\nYou entered: **'{group_members}**.\nPlease try again with your raid group in the following format: **'Player1, Player2, Player 3...'**",
                ephemeral=True,
            )
            return

        raid_name = data_helper.get_cox_raid_name(size, mode)
        time_of_submission = datetime.now()
        formatted_personal_best = personal_best.PersonalBest(
            id=uuid.uuid4(),
            boss=raid_name,
            pb=time,
            approved=False,
            date_achieved=time_of_submission,
            discord_cdn_url=image.url,
            osrs_username=group_members,
            discord_username=interaction.user.display_name,
        )

        id = await self.database.insert_personal_best_submission(
            formatted_personal_best
        )

        embed = await embed_generator.generate_pb_submission_embed(
            title=PENDING + PB_SUBMISSION,
            description=f"Raid name: **{raid_name}**\nTeam Members: **{group_members}**\nTime: **{await convert_pb_to_display_format(time)}**\n",
            color=Colors.yellow,
            timestamp=time_of_submission,
            image_url=image.url,
            footer_id=id,
        )

        message = await approve_channel.send(embed=embed)
        await message.add_reaction("👍")
        await message.add_reaction("👎")
        await interaction.response.send_message(
            "Thank you for your submission. Please wait for an admin to approve :)",
            ephemeral=True,
        )

    # Sub-command to submit TOA PBs
    @group.command(name="toa")
    async def tombs_of_amascut(
        self,
        interaction: discord.Interaction,
        mode: AutoComplete.TOA_MODES,
        group_size: AutoComplete.TOA_GROUPSIZES,
        group_members: str,
        time: PbTimeTransformer,
        image: discord.Attachment,
    ) -> None:
        approve_channel = self.bot.get_channel(ChannelIds.approve_channel)
        size = int(group_size.name)

        if not data_helper.is_valid_group_members_string(group_members, size):
            await interaction.response.send_message(
                f"Group members doesn't match the number of names given for group size of **{size}**.\nYou entered: **'{group_members}**.\nPlease try again with your raid group in the following format: **'Player1, Player2, Player 3...'**",
                ephemeral=True,
            )
            return

        raid_name = data_helper.get_toa_raid_name(size, mode)
        time_of_submission = datetime.now()
        formatted_personal_best = personal_best.PersonalBest(
            id=uuid.uuid4(),
            boss=raid_name,
            pb=time,
            approved=False,
            date_achieved=time_of_submission,
            discord_cdn_url=image.url,
            osrs_username=group_members,
            discord_username=interaction.user.display_name,
        )

        id = await self.database.insert_personal_best_submission(
            formatted_personal_best
        )

        embed = await embed_generator.generate_pb_submission_embed(
            title=PENDING + PB_SUBMISSION,
            description=f"Raid name: **{raid_name}**\nTeam Members: **{group_members}**\nTime: **{await convert_pb_to_display_format(time)}**\n",
            color=Colors.yellow,
            timestamp=time_of_submission,
            image_url=image.url,
            footer_id=id,
        )

        message = await approve_channel.send(embed=embed)
        await message.add_reaction("👍")
        await message.add_reaction("👎")
        await interaction.response.send_message(
            "Thank you for your submission. Please wait for an admin to approve :)",
            ephemeral=True,
        )

    # Sub-command to submit Tzhaar PBs
    @group.command(name="tzhaar")
    @app_commands.autocomplete(boss=AutoComplete.submit_tzhaar_pb_autocomplete)
    async def tzhaar(
        self,
        interaction: discord.Interaction,
        boss: str,
        time: PbTimeTransformer,
        osrs_name: str,
        image: discord.Attachment,
    ) -> None:
        approve_channel = self.bot.get_channel(ChannelIds.approve_channel)

        # TODO - If activity exists in autocomplete

        time_of_submission = datetime.now()
        formatted_personal_best = personal_best.PersonalBest(
            id=uuid.uuid4(),
            boss=boss,
            pb=time,
            approved=False,
            date_achieved=time_of_submission,
            discord_cdn_url=image.url,
            osrs_username=osrs_name,
            discord_username=interaction.user.display_name,
        )

        id = await self.database.insert_personal_best_submission(
            formatted_personal_best
        )

        embed = await embed_generator.generate_pb_submission_embed(
            title=PENDING + PB_SUBMISSION,
            description=f"Tzhaar Activity: **{boss}**\nUsername: **{osrs_name}**\nTime: **{await convert_pb_to_display_format(time)}**\n",
            color=Colors.yellow,
            timestamp=time_of_submission,
            image_url=image.url,
            footer_id=id,
        )

        message = await approve_channel.send(embed=embed)
        await message.add_reaction("👍")
        await message.add_reaction("👎")
        await interaction.response.send_message(
            "Thank you for your submission. Please wait for an admin to approve :)",
            ephemeral=True,
        )

    # Sub-command to submit DT2 PBs
    @group.command(name="dt2")
    @app_commands.autocomplete(boss=AutoComplete.submit_dt2_pb_autocomplete)
    async def dt2(
        self,
        interaction: discord.Interaction,
        boss: str,
        time: PbTimeTransformer,
        osrs_name: str,
        image: discord.Attachment,
    ) -> None:
        approve_channel = self.bot.get_channel(ChannelIds.approve_channel)

        # TODO - If activity exists in autocomplete

        time_of_submission = datetime.now()
        formatted_personal_best = personal_best.PersonalBest(
            id=uuid.uuid4(),
            boss=boss,
            pb=time,
            approved=False,
            date_achieved=time_of_submission,
            discord_cdn_url=image.url,
            osrs_username=osrs_name,
            discord_username=interaction.user.display_name,
        )

        id = await self.database.insert_personal_best_submission(
            formatted_personal_best
        )

        embed = await embed_generator.generate_pb_submission_embed(
            title=PENDING + PB_SUBMISSION,
            description=f"Boss: **{boss}**\nUsername: **{osrs_name}**\nTime: **{await convert_pb_to_display_format(time)}**\n",
            color=Colors.yellow,
            timestamp=time_of_submission,
            image_url=image.url,
            footer_id=id,
        )

        message = await approve_channel.send(embed=embed)
        await message.add_reaction("👍")
        await message.add_reaction("👎")
        await interaction.response.send_message(
            "Thank you for your submission. Please wait for an admin to approve :)",
            ephemeral=True,
        )

    # Submit boss PBs
    @group.command(name="boss")
    @app_commands.autocomplete(boss=AutoComplete.submit_boss_pb_autocomplete)
    async def boss(
        self,
        interaction: discord.Interaction,
        boss: str,
        time: PbTimeTransformer,
        osrs_name: str,
        image: discord.Attachment,
    ) -> None:
        approve_channel = self.bot.get_channel(ChannelIds.approve_channel)

        # TODO - If activity exists in autocomplete

        time_of_submission = datetime.now()
        formatted_personal_best = personal_best.PersonalBest(
            id=uuid.uuid4(),
            boss=boss,
            pb=time,
            approved=False,
            date_achieved=time_of_submission,
            discord_cdn_url=image.url,
            osrs_username=osrs_name,
            discord_username=interaction.user.display_name,
        )

        id = await self.database.insert_personal_best_submission(
            formatted_personal_best
        )

        embed = await embed_generator.generate_pb_submission_embed(
            title=PENDING + PB_SUBMISSION,
            description=f"Boss: **{boss}**\nUsername: **{osrs_name}**\nTime: **{await convert_pb_to_display_format(time)}**\n",
            color=Colors.yellow,
            timestamp=time_of_submission,
            image_url=image.url,
            footer_id=id,
        )

        message = await approve_channel.send(embed=embed)
        await message.add_reaction("👍")
        await message.add_reaction("👎")
        await interaction.response.send_message(
            "Thank you for your submission. Please wait for an admin to approve :)",
            ephemeral=True,
        )

    @group.command(name="misc")  # we use the declared group to make a command.
    @app_commands.autocomplete(activity=AutoComplete.submit_misc_autocomplete)
    async def misc(
        self,
        interaction: discord.Interaction,
        activity: str,
        time: PbTimeTransformer,
        osrs_name: str,
        image: discord.Attachment,
    ) -> None:
        approve_channel = self.bot.get_channel(ChannelIds.approve_channel)

        # TODO - If activity exists in autocomplete

        time_of_submission = datetime.now()
        formatted_personal_best = personal_best.PersonalBest(
            id=uuid.uuid4(),
            boss=activity,
            pb=time,
            approved=False,
            date_achieved=time_of_submission,
            discord_cdn_url=image.url,
            osrs_username=osrs_name,
            discord_username=interaction.user.display_name,
        )

        id = await self.database.insert_personal_best_submission(
            formatted_personal_best
        )

        embed = await embed_generator.generate_pb_submission_embed(
            title=PENDING + PB_SUBMISSION,
            description=f"Misc Activity/Boss: **{activity}**\nUsername: **{osrs_name}**\nTime: **{await convert_pb_to_display_format(time)}**\n",
            color=Colors.yellow,
            timestamp=time_of_submission,
            image_url=image.url,
            footer_id=id,
        )

        message = await approve_channel.send(embed=embed)
        await message.add_reaction("👍")
        await message.add_reaction("👎")
        await interaction.response.send_message(
            "Thank you for your submission. Please wait for an admin to approve :)",
            ephemeral=True,
        )

    # @commands.command()
    # async def build_tob_pbs(self, ctx):
    #     data = await self.database.get_personal_bests()

    #     for groups in theatre_of_blood.INFO:
    #         embeds = []
    #         for boss in groups:
    #             embeds.append(
    #                 await embed_generator.generate_pb_embed(
    #                     data, boss, number_of_placements=3
    #                 )
    #             )
    #         await ctx.send(embeds=embeds)

    # @commands.command()
    # async def build_cox_pbs(self, ctx):
    #     data = await self.database.get_personal_bests()

    #     for groups in chambers_of_xeric.INFO:
    #         embeds = []
    #         for boss in groups:
    #             embeds.append(
    #                 await embed_generator.generate_pb_embed(
    #                     data, boss, number_of_placements=3
    #                 )
    #             )
    #         await ctx.send(embeds=embeds)

    # @commands.command()
    # async def build_toa_pbs(self, ctx):
    #     channel = ctx.channel
    #     data = await self.database.get_personal_bests()

    #     for groups in tombs_of_amascut.INFO:
    #         embeds = []
    #         for boss in groups:
    #             embeds.append(
    #                 await embed_generator.generate_pb_embed(
    #                     data, boss, number_of_placements=3
    #                 )
    #             )
    #         await ctx.send(embeds=embeds)

    # @commands.command()
    # async def build_tzhaar_pbs(self, ctx):
    #     channel = ctx.channel
    #     data = await self.database.get_personal_bests()

    #     for groups in tzhaar.INFO:
    #         embeds = []
    #         for boss in groups:
    #             embeds.append(
    #                 await embed_generator.generate_pb_embed(
    #                     data, boss, number_of_placements=3
    #                 )
    #             )
    #         await ctx.send(embeds=embeds)

    # @commands.command()
    # async def build_dt2_pbs(self, ctx):
    #     channel = ctx.channel
    #     data = await self.database.get_personal_bests()

    #     for groups in dt2bosses.INFO:
    #         embeds = []
    #         for boss in groups:
    #             embeds.append(
    #                 await embed_generator.generate_pb_embed(
    #                     data, boss, number_of_placements=3
    #                 )
    #             )
    #         await ctx.send(embeds=embeds)

    # @commands.command()
    # async def build_boss_pbs(self, ctx):
    #     channel = ctx.channel
    #     data = await self.database.get_personal_bests()

    #     for groups in bosses.INFO:
    #         embeds = []
    #         for boss in groups:
    #             embeds.append(
    #                 await embed_generator.generate_pb_embed(
    #                     data, boss, number_of_placements=3
    #                 )
    #             )
    #         await ctx.send(embeds=embeds)

    # @commands.command()
    # async def build_misc_activities(self, ctx):
    #     channel = ctx.channel
    #     data = await self.database.get_personal_bests()

    #     for groups in misc_activities.INFO:
    #         embeds = []
    #         for boss in groups:
    #             embeds.append(
    #                 await embed_generator.generate_pb_embed(
    #                     data, boss, number_of_placements=3
    #                 )
    #             )
    #         await ctx.send(embeds=embeds)

    # @commands.command()
    # async def how_to_submit(self, ctx):
    #     tutorial_embed = await embed_generator.generate_how_to_submit_embed()
    #     await ctx.send(embed=tutorial_embed)

    async def submit_boss_pb_autocomplete(
        self,
        interaction: discord.Interaction,
        current: str,
    ) -> typing.List[app_commands.Choice[str]]:
        return [app_commands.Choice("boss_name", "boss_name")]

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
        # self.logger.info("Running submit_boss_pb command")

        # approve_channel = self.bot.get_channel(ChannelIds.approve_channel)
        # self.logger.info("Got approved channel")

        # if image is None:
        # await interaction.response.send_message("Please upload an image.")
        # return

        # TODO: check if boss is equal to one in the submit_boss_pb_autocomplete list (spelled correctly. case-sensitive)

        # TODO: This is gonna be used for raids too, once we combine into one submit command. We'll need to maybe do a check for
        # type of PB because I'd like to include different information like: 'Team Members' or 'Group Size'

        # TODO: String building should be done in an embed service/helper

        # description = f"Boss name: **{boss_name}**\nSubmitter: **{osrs_username}** (@{interaction.user.display_name})\nPB: **{await convert_pb_to_display_format(pb)}**\n"

        # self.logger.info("Built the submission embed description")
        # time_of_submission = datetime.now()
        # self.logger.info("Building PersonalBest model")
        # Build the PersonalBest model and insert a record
        # formatted_personal_best = personal_best.PersonalBest(
        #     id=uuid.uuid4(),
        #     boss=boss_name,
        #     pb=pb,
        #     approved=False,
        #     date_achieved=time_of_submission,
        #     discord_cdn_url=image.url,
        #     osrs_username=osrs_username,
        #     discord_username=interaction.user.display_name,
        # )
        # self.logger.info(
        #     "Attempting to insert the PersonalBest into DB with approved: False"
        # )
        # id = await self.database.insert_personal_best_submission(
        #     formatted_personal_best
        # )
        self.logger.info(f"Success! adding record ID '{id}' to embed footer")

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

        message = await self.approve_channel.send(embed=embed)
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
                            f"<@{payload.member.id}> approved the submission! 👍",
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
                            f"<@{payload.member.id}> denied the submission 👎",
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
                    await highscores_service.update_boss_highscores(
                        self, ChannelIds.tob_pbs, theatre_of_blood.INFO
                    )

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
