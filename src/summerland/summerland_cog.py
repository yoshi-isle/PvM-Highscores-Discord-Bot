import logging
import operator
import PIL
import discord
import io
from constants.colors import Colors
from discord import app_commands
from discord.ext import commands
from summerland.constants.channels import ChannelIds
from summerland.constants.tiles import BINGO_TILES
from PIL import Image
from discord import Embed


class Summerland(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.logger = logging.getLogger("discord")
        self.database = self.bot.database
        self.PLACEMENT_EMOJIS = {
            1: "<:1stplacecrown:1201249547737894972> ",
            2: "<:2ndplacecrown:1201249561423917248> ",
            3: "<:3rdplacecrown:1201249572664643664> ",
            4: "",
            5: "",
            6: "",
            7: "",
            8: "",
            9: "",
            10: "",
        }
        self.TEAM_IMAGES = {
            1: "src/summerland/images/piece_team1.png",
            2: "src/summerland/images/piece_team2.png",
            3: "src/summerland/images/piece_team3.png",
            4: "src/summerland/images/piece_team4.png",
            5: "src/summerland/images/piece_team4.png",
            6: "src/summerland/images/piece_team4.png",
            7: "src/summerland/images/piece_team4.png",
            8: "src/summerland/images/piece_team4.png",
            9: "src/summerland/images/piece_team4.png",
            10: "src/summerland/images/piece_team4.png",
        }

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

        await ctx.send(record)

    @commands.command()
    async def force_update_current_standings(
        self,
        ctx: commands.Context,
    ) -> None:
        await ctx.channel.purge()
        await self.update_current_standings()

    @commands.command()
    async def temp_updatetile(
        self,
        ctx: commands.Context,
        tile: int,
    ) -> None:
        await ctx.send(f"Going to tile {tile}")
        await self.database.update_team_tile(
            "1241499583180177469", "current_tile", tile
        )
        record = await self.database.get_team_info("1241499583180177469")

        current = record["tile_history"]
        current.append(tile)
        await self.database.update_team_tile(
            "1241499583180177469", "tile_history", current
        )

    async def update_current_standings(self):
        teams = await self.database.get_all_teams()
        teams = await self.get_top_teams(teams)
        placement = 1
        current_standings_text = await self.generate_current_standings_text(teams)
        current_standings_channel = self.bot.get_channel(ChannelIds.current_standings)

        # Generated board image
        with Image.open("src/summerland/images/theboard_dimmed.png") as img:
            for record in teams:
                team_number = record["team_number"]
                tile_number = record["current_tile"] - 1
                with Image.open(
                    self.TEAM_IMAGES.get(team_number)
                ) as team_board_piece_img:
                    team_board_piece_img = team_board_piece_img.convert("RGBA")
                    position = BINGO_TILES[tile_number]["PieceCoordinate"]
                    img.paste(team_board_piece_img, position, team_board_piece_img)

            img.save("board_with_merged_game_piece_layers.png")
            final_image = discord.File("board_with_merged_game_piece_layers.png")
            await current_standings_channel.send(file=final_image)

        # Top Teams embed
        top_teams_embed = discord.Embed()
        top_teams_embed.title = "__**Top Teams:**__"
        top_teams_embed.add_field(name="", value=current_standings_text, inline=False)
        top_teams_embed.set_thumbnail(
            url="https://oldschool.runescape.wiki/images/thumb/Twisted_dragon_trophy_detail.png/140px-Twisted_dragon_trophy_detail.png?c8c23"
        )
        top_teams_embed.set_footer(text="discord.gg/kittycats")
        top_teams_embed.colour = Colors.light_blue
        await current_standings_channel.send(embed=top_teams_embed)

    async def get_top_teams(self, data):
        """
        Sorts the top teams from the team informations given
        """
        all_teams = (result for result in data)
        return sorted(all_teams, key=operator.itemgetter("current_tile"), reverse=True)

    async def generate_current_standings_text(self, teams):
        current_standings_text = ""
        # Used for ties
        current_placement = 1

        for i in range(len(teams)):
            team_name = str(teams[i]["team_name"])
            tile_number = str(teams[i]["current_tile"])
            tile_name = str(BINGO_TILES[int(tile_number) - 1]["Name"])

            current_standings_text += f"> **{self.PLACEMENT_EMOJIS.get(current_placement)}{team_name} - **Tile {tile_number}: {tile_name}\n"

            # Is the next record a tie?
            if i != len(teams) - 1:
                if teams[i]["current_tile"] > teams[i + 1]["current_tile"]:
                    current_placement = current_placement + 1

        return current_standings_text


async def setup(bot):
    await bot.add_cog(Summerland(bot))
