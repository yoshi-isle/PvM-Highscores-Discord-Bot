import asyncio
import logging
import logging.handlers
from typing import List, Optional

import discord
from discord.ext import commands

from database import Database
from imgur_interface import ImgurInterface
from settings import get_environment_variable
from signup.signup import SignupView
from wise_old_man import WiseOldManClient

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
        self.database = Database()
        self.logger = logging.getLogger("discord")
        self.wom = WiseOldManClient()
        self.imgur = ImgurInterface()

    def __exit__(self, *args):
        self.database._disconnect()
        self.wom._disconnect

    async def setup_hook(self) -> None:
        # here, we are loading extensions prior to sync to ensure we are syncing interactions defined in those extensions.

        for extension in self.initial_extensions:
            try:
                await self.load_extension(extension)
            except discord.ext.commands.ExtensionNotFound as e:
                self.logger.critical("The extension could not be imported. %s" % e)
            except discord.ext.commands.NoEntryPointError as e:
                self.logger.critical("%s" % e)
            except discord.ext.commands.ExtensionFailed as e:
                self.logger.critical(
                    "The extension failed to load during execution %s" % e
                )

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
        bingo_message = self.database.mgmt_collection.find_one(
            {"message_key": "signup message"}
        )
        if bingo_message is not None and bingo_message.get("message id"):
            self.add_view(
                SignupView(team=bingo_message.get("optional_state")),
                message_id=bingo_message.get("message id"),
            )

        await self.wom._connect()


async def main():
    root_logger = logging.getLogger("discord")
    root_logger.setLevel(logging.INFO)

    # file_handler = logging.handlers.RotatingFileHandler(
    #     filename="discord.log",
    #     encoding="utf-8",
    #     maxBytes=32 * 1024 * 1024,  # 32 MiB
    #     backupCount=5,  # Rotate through 5 files
    # )

    dt_fmt = "%Y-%m-%d %H:%M:%S"
    formatter = logging.Formatter(
        "[{asctime}] [{levelname:<8}] {name}: {message}", dt_fmt, style="{"
    )
    # file_handler.setFormatter(formatter)
    # root_logger.addHandler(file_handler)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)

    bot_token = get_environment_variable("BOT_TOKEN")

    intents = discord.Intents.all()
    intents.message_content = True

    initial_extensions = [
        "management.management_cog",
        "management.greetings_cog",
        "static_embed.static_embed_cog",
        "killcount.killcount_cog",
        "hall_of_fame.hall_of_fame_cog",
        "clan_foundation.clan_foundation_cog"
        # "summerland.summerland_cog",
    ]

    async with CustomBot(
        command_prefix="!",
        initial_extensions=initial_extensions,
        intents=intents,
    ) as bot:
        await bot.start(bot_token)


if __name__ == "__main__":
    logger = logging.getLogger("discord")
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Bot interrupted")
    finally:
        logger.info("Successfully shutdown the Bot")
