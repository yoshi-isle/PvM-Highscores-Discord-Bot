import logging
import copy

import discord
from discord import app_commands
from discord.ext import commands
from database import Database
from discord import Embed
from summerland.constants.channelids import ChannelIds
import summerland.constants.tiles as bingo_tiles
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
            await ctx.send("Sorry. Couldn't find any information. Please DM @Yoshe for support")
            return
        
        tile_number = team_info["currentTile"]
        current_tile = bingo_tiles.tiles[tile_number]
        team_name = team_info["teamName"]
        tile_name = current_tile["Title"]

        embed = Embed(
            title=f"Team Info: {team_name}",
            description=f"Current Tile: (#{tile_number}) {tile_name}",
        )

        embed.set_image(url=current_tile["ImageUrl"])
        await ctx.send(embed=embed)

    @commands.command()
    async def test_go_to_tile_4(self, ctx: commands.Context) -> None:
        setinfo = await self.database.set_team_tile(str(ctx.channel.id), 7)
        if ctx.channel.category.id != ChannelIds.summerland_category:
            return
    
    @app_commands.command()
    async def submitter(self, interaction: discord.Interaction, image: discord.Attachment) -> None:
        team_info = await self.database.get_team(str(interaction.channel.id))
        
        tile_number = team_info["currentTile"]
        current_tile = bingo_tiles.tiles[tile_number]
        team_name = team_info["teamName"]
        tile_name = current_tile["Title"]

        embed = Embed(
            title=f"Pending submission from {team_name}",
            description=f"**Tile (#{tile_number}): ** {tile_name}",
        )
        embed.set_footer(text=f"{team_name},{tile_number},{interaction.channel.id}")
        embed.set_image(url=image)
        embed.color = Colors.yellow

        approve_channel = self.bot.get_channel(ChannelIds.summerland_approve)
        message = await approve_channel.send(embed=embed)
        await message.add_reaction("👍")
        await message.add_reaction("👎")
        await interaction.response.send_message(f"# Pending Submission\nYour team submitted an image for: **{tile_name}**. Please wait while an admin approves, then your dice will be automatically rolled!")

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

                # We only want to edit pending submissions
                if "Pending" in embed.title:
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
                        message = await team_channel.send("# 🟢 Congratulations!\nYour submission has been approved! Rolling...")
                        new_tile_number = int(tile_number) + choice
                        message = await team_channel.send(f"You rolled a **{choice}**, landing your team on **{new_tile_number}**")
                        message = await team_channel.send(bingo_tiles.tiles[new_tile_number])
                        team_info = await self.database.set_team_tile(channel_id, new_tile_number)
                        
                        # team_info thingy
                        

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
                        message = await team_channel.send("# 🔴 Hmm...\nYour submission was denied. A bingo moderator will be in touch shortly.")

async def setup(bot):
    await bot.add_cog(Summerland(bot))