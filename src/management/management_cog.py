from typing import Literal, Optional
import logging

import discord
from discord.ext import commands

class Management(commands.Cog):
    @commands.command()
    @commands.guild_only()
    @commands.is_owner()
    async def unload_signup(self,
        ctx: commands.Context,
    ) -> None:
        await self.bot.unload_extension("bingo.signup_cog")
        await ctx.send(
                "Signup has been disabled"
            )

    @commands.command()
    @commands.guild_only()
    @commands.is_owner()
    async def load_signup(self,
        ctx: commands.Context,
    ) -> None:
        await self.bot.load_extension("bingo.signup_cog")
        await ctx.send(
                "Signup has been enabled"
            )

    @commands.command()
    @commands.guild_only()
    @commands.is_owner()
    async def sync(self,
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
        logger = logging.getLogger('discord')
        logger.critical("management cog loaded")

async def setup(bot):
    await bot.add_cog(Management(bot))
