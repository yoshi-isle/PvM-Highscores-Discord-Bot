import discord
from discord import app_commands
from discord.ext import commands

class Bingo(commands.Cog):
    def __init__(self, client: MyClient):
        self.client = client

    @app_commands.command()
    async def ping(self, interaction: discord.Interaction) -> None:
        ping1 = f"{str(round(self.client.latency * 1000))} ms"
        embed = discord.Embed(title = "**Pong!**", description = "**" + ping1 + "**", color = 0xafdafc)
        await interaction.response.send_message(embed = embed)

async def setup(client):
    await client.add_cog(Bingo(client))

    