import discord
from discord import app_commands

from hall_of_fame.time_helpers import convert_pb_to_time, validate_time_format
from hall_of_fame.string_helpers import validate_string_format


class PbTimeTransformer(app_commands.Transformer):
    """
    This facitalies the ability to take in a discord slash command argument and attempt to transform it into a datetime time object.
    Expecting the string to be in form of 00:00:00.00 or 00:00.00. The major difference is if hours are separated out from the minutes or combined.
    """

    async def transform(self, interaction: discord.Interaction, value: str):
        case = await validate_time_format(value)
        if case:
            return await convert_pb_to_time(case, value)

        # this error will get caught by on app command error
        raise discord.app_commands.TransformerError(
            value=value, opt_type=discord.AppCommandOptionType.string
        )


class UsernamesTransformer(app_commands.Transformer):
    """
    This facitalies the ability to take in a discord slash command argument and attempt to transform it into a comma separated string.
    Expecting the string to be in form of "name" or "name1, name2,.."
    """

    async def transform(
        self, interaction: discord.Interaction, value: str, group_size: int
    ):
        case = await validate_string_format(value)
        if case:
            return await value

        # this error will get caught by on app command error
        raise discord.app_commands.TransformerError(
            value=value, opt_type=discord.AppCommandOptionType.string
        )
