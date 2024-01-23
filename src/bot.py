import asyncio
import json
import logging
from typing import Literal, Optional
import discord
from discord import app_commands
from discord.ext import commands

logger = logging.getLogger("discord")
logging.basicConfig(level=logging.WARNING)


# Import keys
with open("../config/appsettings.local.json") as appsettings:
    settings = json.load(appsettings)

bot_token = settings["BotToken"]
channel_id = settings["HighscoresChannelId"]

intents = discord.Intents.all()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    print("Online")


async def load():
    await bot.load_extension("bingo.bingo_cog")
    await bot.load_extension("hall_of_fame.hall_of_fame_cog")


async def main():
    await load()
    await bot.start(bot_token)
    await bot.tree.sync()


@bot.tree.error
async def on_app_command_error(
    interaction: discord.Interaction, error: app_commands.AppCommandError
):
    if isinstance(error, discord.app_commands.TransformerError):
        error_message = f"The following time of **{error.value}** did not conform to the time format. It needs to be in 00:00.00 format"
        await interaction.response.send_message(f"{error_message}", ephemeral=True)



@bot.command()
@commands.guild_only()
@commands.is_owner()
async def sync(ctx: commands.Context, guilds: commands.Greedy[discord.Object], spec: Optional[Literal["~", "*", "^"]] = None) -> None:
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


asyncio.run(main())
