import discord
from discord import app_commands
from hall_of_fame.time_helpers import validate_time_format, convert_pb_to_time

class PbTimeTransformer(app_commands.Transformer):
        async def transform(self, interaction: discord.Interaction, value: str):
            case = await validate_time_format(value)
            if case:
                return await convert_pb_to_time(case, value)

            raise discord.app_commands.TransformerError(value=value, opt_type=discord.AppCommandOptionType.string)