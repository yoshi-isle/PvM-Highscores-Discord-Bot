import logging
import discord
from discord.ext import commands
from PIL import Image

class Candyland(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.logger = logging.getLogger("discord")

    def is_bot(self, message):
        return message.author == self.bot.user

    @commands.Cog.listener()
    async def on_ready(self):
        self.logger.info("candyland cog loaded")

    @commands.command()
    async def candyland_board(
        self,
        ctx: commands.Context,
    ) -> None:
        base_img = Image.open('src/candyland/test_image.png')
        overlay_img = Image.open('src/candyland/test_image_2.png')
        # Convert the overlay image to RGBA mode
        overlay_img = overlay_img.convert('RGBA')

        # Define the position where the overlay image will be pasted
        position = (66, 101)

        # Overlay the image over base image
        base_img.paste(overlay_img, position, overlay_img)

        # Save the resulting image
        base_img.save('overlayed_image.png')

        with open('overlayed_image.png', 'rb') as f:
            picture = discord.File(f)
            await ctx.send(file=picture)

async def setup(bot):
    await bot.add_cog(Candyland(bot))
