import discord
from discord.ext import commands
from PIL import Image, ImageDraw, ImageFont
import aiohttp
import io
import aiosqlite
import os

class Visuals(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.font_path = "assets/OpenSans-VariableFont_wdth,wght.ttf"  # Use a sleek font like Open Sans or Montserrat

    async def generate_xp_card(self, user: discord.User, display_name: str, level: int, xp: int, next_level_xp: int):
        width, height = 700, 180
        bar_width = 400

        # Base card
        card = Image.new("RGBA", (width, height), (20, 20, 20, 255))  # Sleek dark theme
        draw = ImageDraw.Draw(card)

        # Fonts
        font_large = ImageFont.truetype(self.font_path, 28)
        font_small = ImageFont.truetype(self.font_path, 20)

        # Avatar
        async with aiohttp.ClientSession() as session:
            async with session.get(user.display_avatar.url) as resp:
                avatar_bytes = await resp.read()
        avatar = Image.open(io.BytesIO(avatar_bytes)).resize((120, 120)).convert("RGBA")
        mask = Image.new("L", avatar.size, 0)
        mask_draw = ImageDraw.Draw(mask)
        mask_draw.ellipse((0, 0, 120, 120), fill=255)
        avatar.putalpha(mask)
        card.paste(avatar, (30, 30), avatar)

        # Text
        draw.text((170, 30), display_name, font=font_large, fill=(255, 255, 255))
        draw.text((170, 70), f"Level: {level}", font=font_small, fill=(180, 180, 180))
        draw.text((170, 100), f"XP: {xp} / {next_level_xp}", font=font_small, fill=(180, 180, 180))

        # Progress bar
        bar_x, bar_y = 170, 140
        draw.rectangle((bar_x, bar_y, bar_x + bar_width, bar_y + 15), fill=(50, 50, 50))
        progress = int((xp / next_level_xp) * bar_width)
        draw.rectangle((bar_x, bar_y, bar_x + progress, bar_y + 15), fill=(255, 215, 0))  # Gold fill

        # Return image
        with io.BytesIO() as image_binary:
            card.save(image_binary, 'PNG')
            image_binary.seek(0)
            return discord.File(fp=image_binary, filename="xp_card.png")

    @commands.command()
    async def levelcard(self, ctx):
        user = ctx.author
        user_id = user.id

        async with aiosqlite.connect("data/currency.db") as db:
            cursor = await db.execute("SELECT xp FROM users WHERE user_id = ?", (user_id,))
            row = await cursor.fetchone()

        if row is None:
            return await ctx.send("❌ You have no XP yet!")

        xp = row[0]
        level = int(xp ** 0.5 // 10)
        next_level_xp = (level + 1) ** 2 * 100

        display_name = user.display_name or user.name
        card = await self.generate_xp_card(user, display_name, level, xp, next_level_xp)
        await ctx.send(file=card)

async def setup(bot):
    await bot.add_cog(Visuals(bot))
