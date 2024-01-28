import logging
from typing import Literal, Optional

import discord
from discord import app_commands
from discord.ext import commands

from constants.channels import ChannelIds, Guild
from random_greeting import get_random_greeting_url
from random_emoji import get_random_achievement_emoji, get_random_drop_emoji, get_random_floof_emoji


class NewMemberView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(
        label="Wave to say Meowdy!",
        style=discord.ButtonStyle.secondary,
    )
    async def send_gif(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        embed = discord.Embed()
        greetings = " says..."
        embed.set_author(
            name=interaction.user.display_name + greetings,
            icon_url=interaction.user.display_avatar.url,
        )
        embed.set_image(url=await get_random_greeting_url())
        await interaction.response.send_message(embed=embed)


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
    @commands.is_owner()
    async def unload_signup(
        self,
        ctx: commands.Context,
    ) -> None:
        await self.bot.unload_extension("bingo.signup_cog")
        await ctx.send("Signup has been disabled")

    @commands.command()
    @commands.guild_only()
    @commands.is_owner()
    async def load_signup(
        self,
        ctx: commands.Context,
    ) -> None:
        await self.bot.load_extension("bingo.signup_cog")
        await ctx.send("Signup has been enabled")

    @commands.command()
    @commands.guild_only()
    @commands.is_owner()
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

    @commands.command()
    @commands.is_owner()
    async def testnewmember(self, ctx: commands.Context):
        to_send = "Welcome"
        await ctx.send(to_send, view=NewMemberView())

    @commands.Cog.listener()
    async def on_member_join(self, member):
        guild = member.guild
        if guild.system_channel is not None:
            to_send = f"Welcome {member.mention} to {guild.name}!"
            await guild.system_channel.send(to_send, view=NewMemberView())

    @commands.Cog.listener()
    async def on_message(self, message):

        if message.author.bot:
            return
        
        if message.channel == ChannelIds.drops:
            if message.attachments:
                message.add_reaction(await get_random_drop_emoji())
                
        elif message.channel == ChannelIds.floofs:
            if message.attachments:
                message.add_reaction(await get_random_floof_emoji())
        elif message.channel == ChannelIds.achievements:
            if message.attachments:
                message.add_reaction(await get_random_achievement_emoji())
        else:
            return



async def setup(bot):
    await bot.add_cog(Management(bot))
