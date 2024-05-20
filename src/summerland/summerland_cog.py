import logging
import operator
import discord
import summerland.embed_generator as embed_generator
from discord import app_commands
from discord.ext import commands
from summerland.constants.channels import ChannelIds
from summerland.constants.tiles import BINGO_TILES
from summerland.constants.board_piece_images import BOARD_PIECE_IMAGES
from summerland.constants.placement_emojis import PLACEMENT_EMOJIS
from PIL import Image
from discord import Embed


class Summerland(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.logger = logging.getLogger("discord")
        self.database = self.bot.database

    @commands.Cog.listener()
    async def on_ready(self):
        self.logger.info("summerland cog loaded")

    @commands.command()
    async def team_info(
        self,
        ctx: commands.Context,
    ) -> None:
        # Get the ID of the channel we're in
        this_channel_id = ctx.channel.id
        # Make sure it's in the DB
        record = await self.database.get_team_info(this_channel_id)
        if record is None:
            await ctx.send("Sorry. Can't find info for this team.")
            return

        await ctx.send(embed=await embed_generator.generate_team_embed(record))

    @commands.command()
    async def force_update_current_standings(
        self,
        ctx: commands.Context,
    ) -> None:
        await ctx.channel.purge()
        teams = await self.database.get_all_teams()
        teams = await self.get_top_teams(teams)
        current_standings_channel = self.bot.get_channel(ChannelIds.current_standings)

        # Generate board image
        with Image.open("src/summerland/images/board_dimmed.png") as img:
            for record in teams:
                team = record
                with Image.open(
                    BOARD_PIECE_IMAGES.get(team.team_number)
                ) as team_board_piece_img:
                    team_board_piece_img = team_board_piece_img.convert("RGBA")
                    position = team.tile["PieceCoordinate"]
                    img.paste(team_board_piece_img, position, team_board_piece_img)

            img.save("final_board.png")
            final_board_image = discord.File("final_board.png")
            await current_standings_channel.send(file=final_board_image)

        # Generate embed for top teams
        embed_field_text = await self.generate_current_standings_text(teams)
        await current_standings_channel.send(
            embed=await embed_generator.generate_top_teams_embed(embed_field_text)
        )

    async def get_top_teams(self, data):
        """
        Sorts the top teams from the team informations given
        """
        all_teams = (result for result in data)
        return sorted(all_teams, key=operator.itemgetter("current_tile"), reverse=True)

    async def generate_current_standings_text(self, teams):
        current_standings_text = ""
        current_placement = 1

        for i in range(len(teams)):
            current_standings_text += f"> **{PLACEMENT_EMOJIS.get(current_placement)}{teams[i]['team_name']} - **Tile {teams[i]['current_tile']}: {BINGO_TILES[teams[i]['current_tile']]['Name']}\n"

            if i != len(teams[i]) - 1:
                if teams[i]["current_tile"] > teams[i + 1]["current_tile"]:
                    current_placement = current_placement + 1

        return current_standings_text


async def setup(bot):
    await bot.add_cog(Summerland(bot))
