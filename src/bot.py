import asyncio
import json
import logging
import logging.handlers
from typing import List, Optional

from bingo.signup_cog import SignupView

import discord
from discord.ext import commands

# reference https://github.com/Rapptz/discord.py/blob/v2.3.2/examples/advanced_startup.py


class CustomBot(commands.Bot):
    def __init__(
        self,
        *args,
        initial_extensions: List[str],
        testing_guild_id: Optional[int] = None,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.testing_guild_id = testing_guild_id
        self.initial_extensions = initial_extensions

    async def setup_hook(self) -> None:
        # here, we are loading extensions prior to sync to ensure we are syncing interactions defined in those extensions.

        for extension in self.initial_extensions:
            await self.load_extension(extension)

        # In overriding setup hook,
        # we can do things that require a bot prior to starting to process events from the websocket.
        # In this case, we are using this to ensure that once we are connected, we sync for the testing guild.
        # You should not do this for every guild or for global sync, those should only be synced when changes happen.
        if self.testing_guild_id:
            guild = discord.Object(self.testing_guild_id)
            # We'll copy in the global commands to test with:
            self.tree.copy_global_to(guild=guild)
            # followed by syncing to the testing guild.
            await self.tree.sync(guild=guild)

        # This would also be a good place to connect to our database and
        # load anything that should be in memory prior to handling events.
        
        bingo_message_id=1199597817811968110
        self.add_view(SignupView(), message_id=bingo_message_id)


async def main():
    root_logger = logging.getLogger("discord")
    root_logger.setLevel(logging.WARNING)

    file_handler = logging.handlers.RotatingFileHandler(
        filename="discord.log",
        encoding="utf-8",
        maxBytes=32 * 1024 * 1024,  # 32 MiB
        backupCount=5,  # Rotate through 5 files
    )

    dt_fmt = "%Y-%m-%d %H:%M:%S"
    formatter = logging.Formatter(
        "[{asctime}] [{levelname:<8}] {name}: {message}", dt_fmt, style="{"
    )
    file_handler.setFormatter(formatter)
    root_logger.addHandler(file_handler)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)

    # Import keys
    with open("../config/appsettings.local.json") as appsettings:
        settings = json.load(appsettings)

    bot_token = settings["BotToken"]

    intents = discord.Intents.all()
    intents.message_content = True

    initial_extensions = [
        "bingo.bingo_cog",
        "bingo.signup_cog",
        "hall_of_fame.hall_of_fame_cog",
        "management.management_cog",
    ]

    async with CustomBot(
        command_prefix="!",
        initial_extensions=initial_extensions,
        intents=intents,
    ) as bot:
        await bot.start(bot_token)


asyncio.run(main())
