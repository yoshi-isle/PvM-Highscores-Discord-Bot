import asyncio
import copy
import logging
import uuid
from datetime import datetime

import discord
from discord import app_commands
from discord.ext import commands

import constants.forum_data as forum_data
import hall_of_fame.constants.personal_best as personal_best
import hall_of_fame.data_helper as data_helper
from constants.channels import ChannelIds
from constants.colors import Colors
from hall_of_fame import embed_generator
from hall_of_fame.autocompletes.autocompletes import AutoComplete
from hall_of_fame.services import highscores_service
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
        if interaction.channel != self.bot.get_channel(ChannelIds.submit_channel):
            await interaction.response.send_message(
                "Wrong channel. Please go to #submit", ephemeral=True
            )
            return

        approve_channel = self.bot.get_channel(ChannelIds.approve_channel)
        size = int(group_size.name)

        if not data_helper.is_valid_group_members_string(group_members, size):
            await interaction.response.send_message(
                f"Group members doesn't match the number of names given for group size of **{size}**.\nYou entered: '**{group_members}**'.\nPlease try again with your raid group in the following format: **'Player1, Player2, Player 3...'**",
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
            footer_id=f"TOB,{id}",
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
        if interaction.channel != self.bot.get_channel(ChannelIds.submit_channel):
            await interaction.response.send_message(
                "Wrong channel. Please go to #submit", ephemeral=True
            )
            return

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
            footer_id=f"COX,{id}",
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
        if interaction.channel != self.bot.get_channel(ChannelIds.submit_channel):
            await interaction.response.send_message(
                "Wrong channel. Please go to #submit", ephemeral=True
            )
            return

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
            footer_id=f"TOA,{id}",
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
        if interaction.channel != self.bot.get_channel(ChannelIds.submit_channel):
            await interaction.response.send_message(
                "Wrong channel. Please go to #submit", ephemeral=True
            )
            return

        approve_channel = self.bot.get_channel(ChannelIds.approve_channel)

        if not data_helper.valid_boss_name(boss, forum_data.tzhaar.INFO):
            await interaction.response.send_message(
                "That's not a valid boss name. Please try again and select an option from the dropdown.",
                ephemeral=True,
            )
            return

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
            footer_id=f"T,{id}",
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
        if interaction.channel != self.bot.get_channel(ChannelIds.submit_channel):
            await interaction.response.send_message(
                "Wrong channel. Please go to #submit", ephemeral=True
            )
            return

        approve_channel = self.bot.get_channel(ChannelIds.approve_channel)

        if not data_helper.valid_boss_name(boss, forum_data.dt2bosses.INFO):
            await interaction.response.send_message(
                "That's not a valid boss name. Please try again and select an option from the dropdown.",
                ephemeral=True,
            )
            return

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
            footer_id=f"DT,{id}",
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
        if interaction.channel != self.bot.get_channel(ChannelIds.submit_channel):
            await interaction.response.send_message(
                "Wrong channel. Please go to #submit", ephemeral=True
            )
            return

        approve_channel = self.bot.get_channel(ChannelIds.approve_channel)

        if not data_helper.valid_boss_name(boss, forum_data.bosses.INFO):
            await interaction.response.send_message(
                "That's not a valid boss name. Please try again and select an option from the dropdown.",
                ephemeral=True,
            )
            return

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
            footer_id=f"B,{id}",
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
        if interaction.channel != self.bot.get_channel(ChannelIds.submit_channel):
            await interaction.response.send_message(
                "Wrong channel. Please go to #submit", ephemeral=True
            )
            return

        approve_channel = self.bot.get_channel(ChannelIds.approve_channel)

        if not data_helper.valid_boss_name(activity, forum_data.misc_activities.INFO):
            await interaction.response.send_message(
                "That's not a valid boss name. Please try again and select an option from the dropdown.",
                ephemeral=True,
            )
            return

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
            footer_id=f"M,{id}",
        )

        message = await approve_channel.send(embed=embed)
        await message.add_reaction("👍")
        await message.add_reaction("👎")
        await interaction.response.send_message(
            "Thank you for your submission. Please wait for an admin to approve :)",
            ephemeral=True,
        )

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def force_update(self, ctx):
        await highscores_service.update_all_pb_highscores(self)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def build_tob_pbs(self, ctx):
        data = await self.database.get_personal_bests()

        embeds = []
        for groups in forum_data.theatre_of_blood.INFO:
            embeds.append(
                await embed_generator.generate_pb_embed(
                    data, groups, number_of_placements=3
                )
            )
        await ctx.send(embeds=embeds)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def build_cox_pbs(self, ctx):
        data = await self.database.get_personal_bests()

        embeds = []
        for category in forum_data.chambers_of_xeric.INFO:
            embeds.append(
                await embed_generator.generate_pb_embed(
                    data, category, number_of_placements=3
                )
            )
        await ctx.send(embeds=embeds)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def build_toa_pbs(self, ctx):
        data = await self.database.get_personal_bests()
        embeds = []
        for category in forum_data.tombs_of_amascut.INFO:
            embeds.append(
                await embed_generator.generate_pb_embed(
                    data, category, number_of_placements=3
                )
            )
        await ctx.send(embeds=embeds)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def build_tzhaar_pbs(self, ctx):
        data = await self.database.get_personal_bests()
        embeds = []
        for groups in forum_data.tzhaar.INFO:
            embeds.append(
                await embed_generator.generate_pb_embed(
                    data, groups, number_of_placements=3
                )
            )
        await ctx.send(embeds=embeds)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def build_dt2_pbs(self, ctx):
        data = await self.database.get_personal_bests()
        embeds = []
        for groups in forum_data.dt2bosses.INFO:
            embeds.append(
                await embed_generator.generate_pb_embed(
                    data, groups, number_of_placements=3
                )
            )
        await ctx.send(embeds=embeds)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def build_boss_pbs(self, ctx):
        data = await self.database.get_personal_bests()
        embeds = []
        for groups in forum_data.bosses.INFO:
            embeds.append(
                await embed_generator.generate_pb_embed(
                    data, groups, number_of_placements=3
                )
            )
        await ctx.send(embeds=embeds)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def build_misc_activities(self, ctx):
        data = await self.database.get_personal_bests()
        embeds = []
        for groups in forum_data.misc_activities.INFO:
            embeds.append(
                await embed_generator.generate_pb_embed(
                    data, groups, number_of_placements=3
                )
            )
        await ctx.send(embeds=embeds)

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

                    # TODO - good god

                    # approved submission
                    if payload.emoji.name == "👍":
                        await channel.send(
                            f"<@{payload.member.id}> approved the submission! 👍",
                            reference=message,
                        )

                        # upload image to imgur async
                        # grab the description from the embed and split based on new lines
                        # use the first entry which should be the title for the name and title of the imgur post
                        # use the rest for the description
                        loop = asyncio.get_event_loop()
                        embed_description = embed.description.split(sep="\n")
                        name = embed_description.pop(0)
                        config = {"album": None, "name": name, "title": name, "description": embed_description}
                        result = await self.bot.imgur.send_image_async(loop=loop, url=embed.image.url, config=config)

                        # TODO: probably try-catch the embed.footer.text instead of just shoving into an insert
                        result = [x.strip() for x in embed.footer.text.split(",")]
                        uuid = result[1]
                        await self.database.set_personal_best_approved(id=uuid, url=result["link"])
                        new_prefix = APPROVED
                        new_color = Colors.green

                        # TODO - put this code in embed generator
                        # deep copy so that we can update the embed
                        new_embed = copy.deepcopy(embed)
                        new_embed.title = new_prefix + PB_SUBMISSION
                        new_embed.color = new_color
                        await message.edit(embed=new_embed)
                        await message.clear_reactions()
                        await highscores_service.update_all_pb_highscores(self)

                        # TODO - put this code in embed generator
                        new_embed = copy.deepcopy(embed)
                        highscore_channel = data_helper.get_highscore_channel_from_pb(
                            self, embed.footer.text
                        )
                        new_embed.color = None
                        new_embed.title = "New PB :ballot_box_with_check:"
                        new_embed.description += (
                            f"\nRankings: {highscore_channel.mention}"
                        )
                        new_embed.set_footer(text="", icon_url="")

                        message = await highscores_service.post_changelog_record(
                            self, new_embed
                        )
                        await message.add_reaction("🔥")

                    # not approved submission
                    elif payload.emoji.name == "👎":
                        await channel.send(
                            f"<@{payload.member.id}> denied the submission 👎",
                            reference=message,
                        )
                        new_prefix = FAILED
                        new_color = Colors.red

                        # TODO - put this code in embed generator
                        # deep copy so that we can update the embed
                        new_embed = copy.deepcopy(embed)
                        new_embed.title = new_prefix + PB_SUBMISSION
                        new_embed.color = new_color
                        await message.edit(embed=new_embed)
                        await message.clear_reactions()

    # Disable typing in #submit
    @commands.Cog.listener()
    async def on_message(self, message):
        current_channel = self.bot.get_channel(message.channel.id)
        submit_channel = self.bot.get_channel(ChannelIds.submit_channel)
        message_author = message.author

        if current_channel != submit_channel:
            return

        if message_author.bot:
            return  # Prevent recursion

        await message.delete()

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
