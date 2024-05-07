import logging

import discord
from discord.ext import commands
from database import Database
from summerland.constants.channelids import ChannelIds

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

        await ctx.send("> This is team number: **" + str(team_info["teamNumber"]) + "**")
        await ctx.send("> Team Members: **" + str(team_info["teamMembers"]) + "**")
        await ctx.send("> Current Tile: **" + str(team_info["currentTile"]) + "**")

    @commands.command()
    async def test_go_to_tile_4(self, ctx: commands.Context) -> None:
        setinfo = await self.database.set_team_tile(str(ctx.channel.id), 4)
        if ctx.channel.category.id != ChannelIds.summerland_category:
            return

async def setup(bot):
    await bot.add_cog(Summerland(bot))

