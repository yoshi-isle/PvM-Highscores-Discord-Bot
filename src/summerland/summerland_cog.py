import logging
import copy
import typing
import discord
from discord import app_commands
from discord.ext import commands
from database import Database
from discord import Embed
from summerland.constants.channelids import ChannelIds
import summerland.constants.tiles as bingo_tiles
import summerland.summerland_embeds as summerland_embeds
from constants.colors import Colors
from Crypto.Random import random


class Summerland(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.logger = logging.getLogger("discord")
        self.database = self.bot.database

    def is_bot(self, message):
        return message.author == self.bot.user

    @commands.Cog.listener()
    async def on_ready(self):
        self.logger.info("summerland cog loaded")

    @commands.command()
    async def team_info(self, ctx: commands.Context) -> None:
        team_info = await self.database.get_team(str(ctx.channel.id))
        if ctx.channel.category.id != ChannelIds.summerland_category:
            return

        if team_info is None:
            await ctx.send(
                "Sorry. Couldn't find any information. Please DM @Yoshe for support"
            )
            return

        await ctx.send(
            embed=await summerland_embeds.make_team_embed(team_info, bingo_tiles)
        )

    @app_commands.command()
    async def submit(
        self, interaction: discord.Interaction, image: discord.Attachment
    ) -> None:
        team_info = await self.database.get_team(str(interaction.channel.id))

        tile_number = team_info["currentTile"]
        current_tile = bingo_tiles.tiles[tile_number]
        team_name = team_info["teamName"]
        tile_name = current_tile["Title"]

        is_partial = current_tile["SubmissionsRequired"] > 1

        # Regular submission
        embed_description = f"**Tile (#{tile_number}): ** {tile_name}\n\n👍 - **Complete** full tile and roll dice\n👎 - **Deny** (please let the team know why)\n\nIf any hesitation just ask @Tanjiro or @k anao"
        embed_title = f"Pending FULL COMPLETION submission from {team_name}"

        # Partial
        if is_partial:
            embed_description = f"**Tile (#{tile_number}): ** {tile_name}\n\n👍 - **Approve** partial credit\n👎 - **Deny** (please let the team know why)\n🎲 - **FORCE COMPLETE** the tile (in the case of an alternate completion)\n\nIf any hesitation just ask @Tanjiro or @k anao"
            embed_title = f"Pending PARTIAL submission from {team_name}"

        embed = Embed(
            title=embed_title,
            description=embed_description,
        )
        embed.set_footer(text=f"{team_name},{tile_number},{interaction.channel.id}")
        embed.set_image(url=image)
        embed.color = Colors.yellow

        approve_channel = self.bot.get_channel(ChannelIds.summerland_approve)
        message = await approve_channel.send(embed=embed)

        await message.add_reaction("👍")
        await message.add_reaction("👎")

        if is_partial:
            await message.add_reaction("🎲")

        await interaction.response.send_message(
            embed=await summerland_embeds.make_pending_submission_embed(
                interaction.user.display_name, tile_name, image.url
            )
        )

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        """
        This is a check for every reaction that happens
        """
        # ignore the reactions from the bot
        if payload.member.bot:
            return

        # only check the reactions on the approve channel
        channel = self.bot.get_channel(payload.channel_id)
        if channel.id == ChannelIds.summerland_approve:
            # grab the actual message the reaction was to
            message = await channel.fetch_message(payload.message_id)

            # the message must contain an embed
            if message.embeds:
                embed = message.embeds[0]

                footer_text = [x.strip() for x in embed.footer.text.split(",")]
                team_info = await self.database.get_team(str(footer_text[2]))
                tile_number = team_info["currentTile"]
                current_tile = bingo_tiles.tiles[tile_number]
                channel_id = int(footer_text[2])
                team_channel = self.bot.get_channel(channel_id)
                current_progress = team_info["progressCounter"]
                progress_needed = current_tile["SubmissionsRequired"]
                # Full submissions
                if "FULL" in embed.title:
                    # approved submission
                    if payload.emoji.name == "👍":
                        await channel.send(
                            f"<@{payload.member.id}> approved the submission! 👍",
                            reference=message,
                        )
                        new_embed = embed
                        new_embed.title = "[Approved] " + embed.title
                        new_embed.color = Colors.green
                        await message.edit(embed=new_embed)
                        await message.clear_reactions()
                        choice = random.randint(1, 5)
                        message = await team_channel.send(
                            embed=await summerland_embeds.make_approved_submission_embed()
                        )
                        new_tile_number = int(tile_number) + choice
                        await team_channel.send(
                            embed=await summerland_embeds.make_diceroll_embed(
                                choice, new_tile_number
                            )
                        )
                        await team_channel.send("# Below is your new tile:")
                        await self.database.set_team_tile(channel_id, new_tile_number)
                        team_info = await self.database.get_team(str(footer_text[2]))
                        await team_channel.send(
                            embed=await summerland_embeds.make_team_embed(
                                team_info, bingo_tiles
                            )
                        )

                    # not approved submission
                    elif payload.emoji.name == "👎":
                        await channel.send(
                            f"<@{payload.member.id}> denied the submission 👎",
                            reference=message,
                        )
                        new_embed = copy.deepcopy(embed)
                        new_embed.title = "[Denied] " + embed.title
                        new_embed.color = Colors.red
                        await message.edit(embed=new_embed)
                        await message.clear_reactions()
                        footer_text = [x.strip() for x in embed.footer.text.split(",")]
                        await team_channel.send(
                            embed=await summerland_embeds.make_denied_submission_embed()
                        )
                # Full submissions
                if "PARTIAL" in embed.title:
                    # approved partial submission
                    if payload.emoji.name == "👍":
                        await self.database.increment_progress(channel_id)
                        current_progress = current_progress + 1
                        await channel.send(
                            f"<@{payload.member.id}> approved the partial submission! Putting them at ({current_progress}/{progress_needed}) 👍",
                            reference=message,
                        )
                        new_embed = embed
                        new_embed.title = "[Approved] " + embed.title
                        new_embed.color = Colors.green
                        await message.edit(embed=new_embed)
                        await message.clear_reactions()
                        choice = random.randint(1, 5)
                        message = await team_channel.send(
                            embed=await summerland_embeds.make_partially_approved_submission_embed(
                                current_progress, progress_needed
                            )
                        )
                        if current_progress >= progress_needed:
                            choice = random.randint(1, 5)
                            message = await team_channel.send(
                                embed=await summerland_embeds.make_approved_submission_embed()
                            )
                            new_tile_number = int(tile_number) + choice
                            await team_channel.send(
                                embed=await summerland_embeds.make_diceroll_embed(
                                    choice, new_tile_number
                                )
                            )
                            await team_channel.send("# Below is your new tile:")
                            await self.database.set_team_tile(
                                channel_id, new_tile_number
                            )
                            team_info = await self.database.get_team(
                                str(footer_text[2])
                            )
                            await team_channel.send(
                                embed=await summerland_embeds.make_team_embed(
                                    team_info, bingo_tiles
                                )
                            )

                    # not approved submission
                    elif payload.emoji.name == "👎":
                        await channel.send(
                            f"<@{payload.member.id}> denied the submission 👎",
                            reference=message,
                        )
                        new_embed = copy.deepcopy(embed)
                        new_embed.title = "[Denied] " + embed.title
                        new_embed.color = Colors.red
                        await message.edit(embed=new_embed)
                        await message.clear_reactions()
                        footer_text = [x.strip() for x in embed.footer.text.split(",")]
                        await team_channel.send(
                            embed=await summerland_embeds.make_denied_submission_embed()
                        )
                    # approved submission
                    elif payload.emoji.name == "🎲":
                        await channel.send(
                            f"<@{payload.member.id}> approved the submission! 👍",
                            reference=message,
                        )
                        new_embed = embed
                        new_embed.title = "[Approved] " + embed.title
                        new_embed.color = Colors.green
                        await message.edit(embed=new_embed)
                        await message.clear_reactions()
                        choice = random.randint(1, 5)
                        message = await team_channel.send(
                            embed=await summerland_embeds.make_approved_submission_embed()
                        )
                        new_tile_number = int(tile_number) + choice
                        await team_channel.send(
                            embed=await summerland_embeds.make_diceroll_embed(
                                choice, new_tile_number
                            )
                        )
                        await team_channel.send("# Below is your new tile:")
                        await self.database.set_team_tile(channel_id, new_tile_number)
                        team_info = await self.database.get_team(str(footer_text[2]))
                        await team_channel.send(
                            embed=await summerland_embeds.make_team_embed(
                                team_info, bingo_tiles
                            )
                        )


async def setup(bot):
    await bot.add_cog(Summerland(bot))
