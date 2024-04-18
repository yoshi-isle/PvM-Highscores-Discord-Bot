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
    async def candyland_board_sample(
        self,
        ctx: commands.Context,
    ) -> None:
        base_img = Image.open('src/candyland/test_image.png')
        overlay_img1 = Image.open('src/candyland/test_image_2.png')
        overlay_img2 = Image.open('src/candyland/test_image_3.png')

        # Convert the overlay image to RGBA mode
        overlay_img1 = overlay_img1.convert('RGBA')
        overlay_img2 = overlay_img2.convert('RGBA')
        # Define the position where the overlay image will be pasted
        position1 = (42, 65)
        position2 = (121, 129)

        # Overlay the image over base image
        base_img.paste(overlay_img1, position1, overlay_img1)
        base_img.paste(overlay_img2, position2, overlay_img2)

        # Save the resulting image
        base_img.save('overlayed_image.png')

        with open('overlayed_image.png', 'rb') as f:
            picture = discord.File(f)
            await ctx.send(file=picture)
        
        await ctx.send("**Current Standings**\n```1st place - Blue Team\n2nd place - Red Team```")

async def setup(bot):
    await bot.add_cog(Candyland(bot))
