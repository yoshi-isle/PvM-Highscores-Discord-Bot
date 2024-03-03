import logging
from typing import Literal, Optional

import discord
from constants.channels import ChannelIds
from discord import app_commands
from discord.ext import commands
from management.random_emoji import (get_random_achievement_emoji,
                                     get_random_drop_emoji,
                                     get_random_floof_emoji)


class Management(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.logger = logging.getLogger("discord")
        self.ctx_menu = app_commands.ContextMenu(
            name="Report to Mods",
            callback=self.report_message,
        )
        self.bot.tree.add_command(self.ctx_menu)

    @commands.command()
    @commands.guild_only()
    @commands.has_role("Admin")
    async def unload_cog(self, ctx: commands.Context, cog: str) -> None:
        await self.bot.unload_extension(cog)
        await ctx.send(f"{cog} has been disabled")

    @commands.command()
    @commands.guild_only()
    @commands.has_role("Admin")
    async def load_cog(self, ctx: commands.Context, cog: str) -> None:
        await self.bot.load_extension(cog)
        await ctx.send(f"{cog} has been enabled")

    @commands.command()
    @commands.guild_only()
    @commands.has_role("Admin")
    async def sync(
        self,
        ctx: commands.Context,
        guilds: commands.Greedy[discord.Object],
        spec: Optional[Literal["~", "*", "^"]] = None,
    ) -> None:
        if not guilds:
            if spec == "~":
                synced = await ctx.bot.tree.sync(guild=ctx.guild)
            elif spec == "*":
                ctx.bot.tree.copy_global_to(guild=ctx.guild)
                synced = await ctx.bot.tree.sync(guild=ctx.guild)
            elif spec == "^":
                ctx.bot.tree.clear_commands(guild=ctx.guild)
                await ctx.bot.tree.sync(guild=ctx.guild)
                synced = []
            else:
                synced = await ctx.bot.tree.sync()

            await ctx.send(
                f"Synced {len(synced)} commands {'globally' if spec is None else 'to the current guild.'}"
            )
            return

        ret = 0
        for guild in guilds:
            try:
                await ctx.bot.tree.sync(guild=guild)
            except discord.HTTPException:
                pass
            else:
                ret += 1

        await ctx.send(f"Synced the tree to {ret}/{len(guilds)}.")

    @commands.Cog.listener()
    async def on_ready(self):
        self.logger.info("management cog loaded")

    async def report_message(
        self, interaction: discord.Interaction, message: discord.Message
    ):
        # We're sending this response message with ephemeral=True, so only the command executor can see it
        await interaction.response.send_message(
            f"Thanks for reporting this message by {message.author.mention} to our moderators.",
            ephemeral=True,
        )

        # Handle report by sending it into a log channel
        log_channel = interaction.guild.get_channel(ChannelIds.admin_notifications)

        embed = discord.Embed(title="Reported Message")
        if message.content:
            embed.description = message.content

        embed.set_author(
            name=message.author.display_name, icon_url=message.author.display_avatar.url
        )
        embed.timestamp = message.created_at

        url_view = discord.ui.View()
        url_view.add_item(
            discord.ui.Button(
                label="Go to Message",
                style=discord.ButtonStyle.url,
                url=message.jump_url,
            )
        )

        await log_channel.send(embed=embed, view=url_view)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        emoji_id = ""
        if message.channel.id == ChannelIds.drops:
            if message.attachments:
                emoji_id = await get_random_drop_emoji()
        elif message.channel.id == ChannelIds.floofs:
            if message.attachments:
                emoji_id = await get_random_floof_emoji()
        elif message.channel.id == ChannelIds.achievements:
            if message.attachments:
                emoji_id = await get_random_achievement_emoji()
        else:
            return

        if emoji_id:
            try:
                await message.add_reaction(emoji_id)
            except discord.NotFound as e:
                self.logger.warning("%s was not found. %s" % (emoji_id, e))
            except discord.HTTPException as e:
                self.logger.warning("%s had some sort of issue. %s" % (emoji_id, e))


async def setup(bot):
    await bot.add_cog(Management(bot))
