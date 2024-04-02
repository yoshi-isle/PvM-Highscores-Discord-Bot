import asyncio
import copy
import logging
import uuid
from asyncio import sleep
from datetime import datetime, time
from enum import Enum

import discord
from discord import app_commands
from discord.ext import commands

import constants.forum_data as forum_data
import hall_of_fame.constants.personal_best as personal_best
import hall_of_fame.data_helper as data_helper
from constants.channels import ChannelIds
from constants.colors import Colors
from constants.forum_data import (bosses, chambers_of_xeric, dt2bosses,
                                  misc_activities, theatre_of_blood,
                                  tombs_of_amascut, trials)
from hall_of_fame import embed_generator
from hall_of_fame.autocompletes.autocompletes import AutoComplete
from hall_of_fame.services import highscores_service
from hall_of_fame.time_helpers import convert_pb_to_display_format
from hall_of_fame.transformers import PbTimeTransformer


PENDING = "Pending "
APPROVED = "Approved "
FAILED = "Failed "
UNDER_MAINTENANCE = "Under Maintenance "
PB_SUBMISSION = "PB Submission"


async def is_valid_iso_time(time_str: str) -> bool:
    """
    Test if a string could convert to a datet time object successfully.
    """
    try:
        datetime.strptime(time_str, "%H:%M:%S.%f")
        return True
    except ValueError:
        return False


async def is_valid_boss(category: str, boss: str) -> bool:
    """
    Test if a boss name exists in the respective catergory.
    """
    if category == "TOA":
        return any(info["boss_name"] == boss for info in tombs_of_amascut.INFO)
    elif category == "TOB":
        return any(info["boss_name"] == boss for info in theatre_of_blood.INFO)
    elif category == "COX":
        return any(info["boss_name"] == boss for info in chambers_of_xeric.INFO)
    elif category == "T":
        return any(info["boss_name"] == boss for info in trials.INFO)
    elif category == "DT":
        return any(info["boss_name"] == boss for info in dt2bosses.INFO)
    elif category == "B":
        return any(info["boss_name"] == boss for info in bosses.INFO)
    elif category == "M":
        return any(info["boss_name"] == boss for info in misc_activities.INFO)
    else:
        return False


class UpdatePbModal(discord.ui.Modal, title="Update this PB Submission"):
    """
    Discord view modal to update a pb submission
    """

    def __init__(self, message: discord.message, database, pb, raid):
        self.message = message
        self.uuid = pb["_id"]
        self.database = database
        self.pb = pb
        self.raid = raid
        super().__init__()

    new_boss = discord.ui.TextInput(
        style=discord.TextStyle.short,
        label="Boss or Activity",
        required=True,
        default="",
    )

    new_names = discord.ui.TextInput(style=discord.TextStyle.short, label="Member Name(s)", required=True, default="")

    new_time = discord.ui.TextInput(style=discord.TextStyle.short, label="Time", required=True, default="")

    async def on_submit(self, interaction: discord.Interaction):
        # time for pb validation
        if not await is_valid_iso_time(self.new_time.value):
            await interaction.response.send_message(
                f"The time '{self.new_time.value}' that was entered was not a valid format. Try again",
                ephemeral=True,
            )
            return

        # Boss name must be in the category it comes from
        if not await is_valid_boss(self.raid, self.new_boss.value):
            await interaction.response.send_message(
                f"The boss '{self.new_boss.value}' that was entered was not a valid boss for the category {self.raid}. Try again",
                ephemeral=True,
            )
            return

        # Number names must match the original number of names
        if len(self.new_names.value.split(",")) != len(self.pb["osrs_username"].split(",")):
            await interaction.response.send_message("Number of names was mismatched. Try again", ephemeral=True)
            return

        # grab the embed and description twice to compare later
        new_embed = self.message.embeds[0]
        old_description = new_embed.description.split(sep="\n")
        new_description = new_embed.description.split(sep="\n")

        # Check for differences and make updates to the database if needed
        # TODO: consolidate to 1 call
        if self.new_boss.value != self.pb["boss"]:
            new_description[0] = old_description[0].replace(self.pb["boss"], self.new_boss.value)
            await self.database.update_personal_best(self.uuid, "boss", self.new_boss.value)

        if self.new_names.value != self.pb["osrs_username"]:
            new_description[1] = old_description[1].replace(self.pb["osrs_username"], self.new_names.value)
            await self.database.update_personal_best(self.uuid, "osrs_username", self.new_names.value)

        if self.new_time.value != self.pb["pb"]:
            new_description[2] = old_description[2].replace(
                await convert_pb_to_display_format(time.fromisoformat(self.pb["pb"])),
                await convert_pb_to_display_format(time.fromisoformat(self.new_time.value)),
            )
            await self.database.update_personal_best(self.uuid, "pb", self.new_time.value)

        change_list = [f"'{old}' was changed to '{new}'" for old, new in zip(old_description, new_description) if old != new]
        changes = "\n".join(change_list)

        new_description = "\n".join(new_description)
        new_embed.title = PENDING + PB_SUBMISSION
        new_embed.description = new_description
        new_embed.color = Colors.yellow

        await self.message.edit(embed=new_embed)
        await self.message.add_reaction("👍")
        await self.message.add_reaction("👎")

        if changes:
            await interaction.response.send_message(
                f"<@{interaction.user.id}> edited this submission {self.message.jump_url} with the following changes:\n" + changes
            )
        else:
            await interaction.response.send_message(f"<@{interaction.user.id}> reverted this submission {self.message.jump_url}")

    async def on_error(self, interaction: discord.Interaction):
        await interaction.response.send_message("Oops! Something went wrong.", ephemeral=True)


class HallOfFame(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.logger = logging.getLogger("discord")
        self.database = self.bot.database
        self.ctx_menu = app_commands.ContextMenu(
            name="Update Pb Submission",
            callback=self.update_pb,
        )
        self.bot.tree.add_command(self.ctx_menu)

    group = app_commands.Group(
        name="submit",
        description="Submit a PB",
    )

    async def get_boss_activity_string(self, raid_type, boss_or_raid) -> str:
        """
        Generate a formated string based on raid type and boss or raid name.
        Args:
            raid_type (_type_): _description_
            boss_or_raid (_type_): _description_

        Returns:
            _type_: _description_
        """
        if raid_type in ["TOA", "TOB", "COX"]:
            return f"Raid name: **{boss_or_raid}**"
        elif raid_type == "T":
            return f"Trial Activity: **{boss_or_raid}**"
        elif raid_type == "DT":
            return f"Boss: **{boss_or_raid}**"
        elif raid_type == "B":
            return f"Boss: **{boss_or_raid}**"
        elif raid_type == "M":
            return f"Misc Activity/Boss: **{boss_or_raid}**"

    async def get_participants_string(self, group_size, group_members):
        if group_size is not None:
            return f"Team Members: **{group_members}**"
        else:
            return f"Username: **{group_members}**"

    async def submit_pb(
        self,
        interaction: discord.Interaction,
        mode: Enum,
        group_size: Enum,
        group_members: str,
        time: time,
        image: discord.Attachment,
        raid_type: str,
        activity: str,
    ):
        # For group content, check that the number of people matches how many names were entered
        if group_size is not None:
            size = int(group_size.name)
            if not await data_helper.is_valid_group_members_string(group_members, size):
                await interaction.response.send_message(
                    f"Group members doesn't match the number of names given for group size of **{size}**.\nYou entered: '**{group_members}**'.\nPlease try again with your raid group in the following format: **'Player1, Player2, Player 3...'**",
                    ephemeral=True,
                )

                return

        boss_or_raid = activity
        # For Raids, we need a formated string for the type of raid and size of party
        if raid_type in ["TOB", "TOA", "COX"]:
            boss_or_raid = await data_helper.get_raid_name(raid_type, size, mode.name)

        time_of_submission = datetime.now()
        formatted_personal_best = personal_best.PersonalBest(
            id=uuid.uuid4(),
            boss=boss_or_raid,
            pb=time,
            approved=False,
            date_achieved=time_of_submission,
            discord_cdn_url=image.url,
            osrs_username=group_members,
            discord_username=interaction.user.display_name,
        )
        id = await self.database.insert_personal_best_submission(formatted_personal_best)

        boss_activity = await self.get_boss_activity_string(raid_type=raid_type, boss_or_raid=boss_or_raid)
        participants = await self.get_participants_string(group_size=group_size, group_members=group_members)

        embed = await embed_generator.generate_pb_submission_embed(
            title=PENDING + PB_SUBMISSION,
            description=f"{boss_activity}\n{participants}\nTime: **{await convert_pb_to_display_format(time)}**\n",
            color=Colors.yellow,
            timestamp=time_of_submission,
            image_url=image.url,
            footer_id=f"{raid_type},{id}",
        )
        approve_channel = self.bot.get_channel(ChannelIds.approve_channel)
        message = await approve_channel.send(embed=embed)
        await message.add_reaction("👍")
        await message.add_reaction("👎")
        await interaction.response.send_message(
            "Thank you for your submission. Please wait for an admin to approve :)",
            ephemeral=True,
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
            await interaction.response.send_message("Wrong channel. Please go to #submit", ephemeral=True)
            return

        await self.submit_pb(
            interaction=interaction,
            mode=mode,
            group_size=group_size,
            group_members=group_members,
            time=time,
            image=image,
            raid_type="TOB",
            activity=None,
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
            await interaction.response.send_message("Wrong channel. Please go to #submit", ephemeral=True)
            return

        await self.submit_pb(
            interaction=interaction,
            mode=mode,
            group_size=group_size,
            group_members=group_members,
            time=time,
            image=image,
            raid_type="COX",
            activity=None,
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
            await interaction.response.send_message("Wrong channel. Please go to #submit", ephemeral=True)
            return

        await self.submit_pb(
            interaction=interaction,
            mode=mode,
            group_size=group_size,
            group_members=group_members,
            time=time,
            image=image,
            raid_type="TOA",
            activity=None,
        )

    # Sub-command to submit Trial PBs
    @group.command(name="trials")
    @app_commands.autocomplete(boss=AutoComplete.submit_trial_pb_autocomplete)
    async def trials(
        self,
        interaction: discord.Interaction,
        boss: str,
        time: PbTimeTransformer,
        osrs_name: str,
        image: discord.Attachment,
    ) -> None:
        if interaction.channel != self.bot.get_channel(ChannelIds.submit_channel):
            await interaction.response.send_message("Wrong channel. Please go to #submit", ephemeral=True)
            return

        if not data_helper.valid_boss_name(boss, forum_data.trials.INFO):
            await interaction.response.send_message(
                "That's not a valid boss name. Please try again and select an option from the dropdown.",
                ephemeral=True,
            )
            return

        await self.submit_pb(
            interaction=interaction,
            mode=None,
            group_size=None,
            group_members=osrs_name,
            time=time,
            image=image,
            raid_type="T",
            activity=boss,
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
            await interaction.response.send_message("Wrong channel. Please go to #submit", ephemeral=True)
            return

        if not data_helper.valid_boss_name(boss, forum_data.dt2bosses.INFO):
            await interaction.response.send_message(
                "That's not a valid boss name. Please try again and select an option from the dropdown.",
                ephemeral=True,
            )
            return

        await self.submit_pb(
            interaction=interaction,
            mode=None,
            group_size=None,
            group_members=osrs_name,
            time=time,
            image=image,
            raid_type="DT",
            activity=boss,
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
            await interaction.response.send_message("Wrong channel. Please go to #submit", ephemeral=True)
            return

        if not data_helper.valid_boss_name(boss, forum_data.bosses.INFO):
            await interaction.response.send_message(
                "That's not a valid boss name. Please try again and select an option from the dropdown.",
                ephemeral=True,
            )
            return

        await self.submit_pb(
            interaction=interaction,
            mode=None,
            group_size=None,
            group_members=osrs_name,
            time=time,
            image=image,
            raid_type="B",
            activity=boss,
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
            await interaction.response.send_message("Wrong channel. Please go to #submit", ephemeral=True)
            return

        if not data_helper.valid_boss_name(activity, forum_data.misc_activities.INFO):
            await interaction.response.send_message(
                "That's not a valid boss name. Please try again and select an option from the dropdown.",
                ephemeral=True,
            )
            return

        await self.submit_pb(
            interaction=interaction,
            mode=None,
            group_size=None,
            group_members=osrs_name,
            time=time,
            image=image,
            raid_type="M",
            activity=activity,
        )

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def force_update(self, ctx):
        updated_amount = await highscores_service.update_all_pb_highscores(self)
        await ctx.send(f"Updated: **{updated_amount}** PBs")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def build_tob_pbs(self, ctx):
        data = await self.database.get_personal_bests()

        embeds = []
        for groups in forum_data.theatre_of_blood.INFO:
            embeds.append(await embed_generator.generate_pb_embed(data, groups, number_of_placements=3))
        await ctx.send(embeds=embeds)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def build_cox_pbs(self, ctx):
        data = await self.database.get_personal_bests()

        embeds = []
        for category in forum_data.chambers_of_xeric.INFO:
            embeds.append(await embed_generator.generate_pb_embed(data, category, number_of_placements=3))
        await ctx.send(embeds=embeds)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def build_toa_pbs(self, ctx):
        data = await self.database.get_personal_bests()
        embeds = []
        for category in forum_data.tombs_of_amascut.INFO:
            embeds.append(await embed_generator.generate_pb_embed(data, category, number_of_placements=3))
        await ctx.send(embeds=embeds)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def build_trial_pbs(self, ctx):
        data = await self.database.get_personal_bests()
        embeds = []
        for groups in forum_data.trials.INFO:
            embeds.append(await embed_generator.generate_pb_embed(data, groups, number_of_placements=3))
        await ctx.send(embeds=embeds)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def build_dt2_pbs(self, ctx):
        data = await self.database.get_personal_bests()
        embeds = []
        for groups in forum_data.dt2bosses.INFO:
            embeds.append(await embed_generator.generate_pb_embed(data, groups, number_of_placements=3))
        await ctx.send(embeds=embeds)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def build_boss_pbs(self, ctx):
        data = await self.database.get_personal_bests()
        embeds = []
        for groups in forum_data.bosses.INFO:
            embeds.append(await embed_generator.generate_pb_embed(data, groups, number_of_placements=3))
        await ctx.send(embeds=embeds)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def build_misc_activities(self, ctx):
        data = await self.database.get_personal_bests()
        embeds = []
        for groups in forum_data.misc_activities.INFO:
            embeds.append(await embed_generator.generate_pb_embed(data, groups, number_of_placements=3))
        await ctx.send(embeds=embeds)

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
                        # grab the description from the embed, remove all astericks, and split based on new lines
                        # use the first entry which should be the title for the name and title of the imgur post
                        # use the rest for the description
                        loop = asyncio.get_event_loop()
                        embed_description = embed.description.replace("*", "").split(sep="\n")
                        name = embed_description.pop(0)
                        config = {
                            "album": None,
                            "name": name,
                            "title": name,
                            "description": "\n".join(embed_description),
                        }
                        
                        sleep_duration = 2
                        for retries in range(2):
                            imgur_result = await self.bot.imgur.send_image_async(loop=loop, url=embed.image.url, config=config)
                            if imgur_result.status_code == 200:
                                self.logger.info("imgur credit info: %s" % self.bot.imgur.client.credits)
                                break
                            else:
                                sleep_duration = pow(sleep_duration,retries)
                                await sleep(sleep_duration) 
                              
                        if imgur_result.status_code == 200:
                            # TODO: probably try-catch the embed.footer.text instead of just shoving into an insert
                            result = [x.strip() for x in embed.footer.text.split(",")]
                            uuid = result[1]
                            await self.database.set_personal_best_approved(id=uuid, url=imgur_result["link"])
                            new_prefix = APPROVED
                            new_color = Colors.green
    
                            # TODO - put this code in embed generator
                            # deep copy so that we can update the embed
                            new_embed = embed
                            new_embed.title = new_prefix + PB_SUBMISSION
                            new_embed.color = new_color
                            await message.edit(embed=new_embed)
                            await message.clear_reactions()
                            _ = await highscores_service.update_all_pb_highscores(self)
    
                            highscore_channel = data_helper.get_highscore_channel_from_pb(self, embed.footer.text)
                            new_embed.color = None
                            new_embed.title = "New PB :ballot_box_with_check:"
                            new_embed.description += f"\nRankings: {highscore_channel.mention}"
                            new_embed.set_footer(text="", icon_url="")
    
                            message = await highscores_service.post_changelog_record(self, new_embed)
                            await message.add_reaction("🔥")
                        else:
                            await channel.send(
                              "Something went wrong with imgur upload. Check the logs",
                              reference=message,
                          )

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

    async def update_pb(self, interaction: discord.Interaction, message: discord.Message):
        # ignore messages not from the bot
        if not message.author.bot:
            return

        # Must be on the approve channel
        channel = self.bot.get_channel(message.channel.id)
        if not channel.id == ChannelIds.approve_channel:
            return

        # The message must have an embed
        if not message.embeds:
            return

        # The submission must have pending or  under in title
        embed = message.embeds[0]
        if "Pending" not in embed.title and "Under" not in embed.title:
            return

        # set embed to maintenance and clear emojis
        new_prefix = UNDER_MAINTENANCE
        new_color = Colors.tangerine
        new_embed = copy.deepcopy(embed)
        new_embed.title = new_prefix + PB_SUBMISSION
        new_embed.color = new_color
        await message.edit(embed=new_embed)
        await message.clear_reactions()

        # get message and extract info
        footer_text = [x.strip() for x in embed.footer.text.split(",")]
        uuid = footer_text[1]
        pb = await self.database.get_personal_best_by_id(id=uuid)

        # push view with existing data as default values
        modal = UpdatePbModal(message, self.database, pb, footer_text[0])
        modal.new_boss.default = pb["boss"]
        modal.new_time.default = pb["pb"]
        modal.new_names.default = pb["osrs_username"]
        await interaction.response.send_modal(modal)

    async def cog_app_command_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        if isinstance(error, discord.app_commands.TransformerError):
            error_message = f"The following time of **{error.value}** did not conform to the time format. It needs to be in 00:00.00 format"
            await interaction.response.send_message(f"{error_message}", ephemeral=True)

    @commands.Cog.listener()
    async def on_ready(self):
        self.logger.info("hof cog loaded")


async def setup(bot):
    await bot.add_cog(HallOfFame(bot))
