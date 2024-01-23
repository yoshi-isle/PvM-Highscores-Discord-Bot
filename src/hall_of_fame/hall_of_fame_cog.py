import json
import typing
import uuid
from datetime import datetime

import discord
from discord import app_commands
from discord.ext import commands

import constants.boss_names as boss_names
import constants.raid_names as raid_info
import hall_of_fame.constants.personal_best as personal_best
import hall_of_fame.database as database
from constants.colors import Colors
from hall_of_fame import embed_generator
from hall_of_fame.time_helpers import (convert_pb_to_display_format,
                                       convert_time_to_microseconds)
from hall_of_fame.transformers import PbTimeTransformer

PENDING = "Pending "
APPROVED = "Approved "
FAILED = "Failed "
PB_SUBMISSION = "PB Submission"


class HallOfFame(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

        with open("../config/appsettings.local.json") as appsettings:
            self.data = json.load(appsettings)

    @commands.command()
    async def raidpbs(self, ctx):
        channel = ctx.channel
        await channel.purge()
        data = database.get_personal_bests()

        for info in raid_info.RAID_INFO:
            await embed_generator.post_raids_embed(
                ctx,
                data,
                info,
                pb_categories=raid_info.RAID_INFO[info],
                number_of_placements=3,
            )

    @commands.command()
    async def bosspbs(self, ctx):
        channel = ctx.channel
        await channel.purge()
        data = database.get_personal_bests()

        for name in boss_names.BOSS_NAMES:
            await embed_generator.post_boss_embed(
                ctx, data, name, number_of_placements=3
            )

    async def submit_boss_pb_autocomplete(
        self,
        interaction: discord.Interaction,
        current: str,
    ) -> typing.List[app_commands.Choice[str]]:
        data = []
        for boss_name in boss_names.BOSS_NAMES:
            if current.lower() in boss_name.lower():
                data.append(app_commands.Choice(name=boss_name, value=boss_name))
        return data

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
        approve_channel = self.bot.get_channel(self.data["ApproveChannelId"])

        if image is None:
            await interaction.response.send_message("Please upload an image.")
            return

        # Todo: check if boss is equal to one in the submit_boss_pb_autocomplete list (spelled correctly. case-sensitive)

        description = f"@{interaction.user.display_name} is submitting a PB of: {await convert_pb_to_display_format(pb)} for **{boss_name}**!\n\nClick the '👍' to approve."

        time_of_submission = datetime.now()

        # Build the PersonalBest model and insert a record
        formatted_personal_best = personal_best.PersonalBest(
            id=uuid.uuid4(),
            boss=boss_name,
            pb=await convert_time_to_microseconds(pb),
            approved=False,
            date_achieved=time_of_submission,
            discord_cdn_url=image.url,
            osrs_username=osrs_username,
            discord_username=interaction.user.display_name,
        )

        id = database.insert_pending_submission(formatted_personal_best)

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


async def setup(bot):
    await bot.add_cog(HallOfFame(bot))
