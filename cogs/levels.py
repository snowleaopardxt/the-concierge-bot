import discord
from discord.ext import commands
import aiosqlite

class Leveling(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def xp_for_level(self, level: int) -> int:
        return 50 * (level ** 2) + 50 * level

    def calculate_level(self, xp: int) -> int:
        level = 0
        while xp >= self.xp_for_level(level):
            level += 1
        return level

    def generate_progress_bar(self, percent: float, length: int = 10) -> str:
        filled = int(percent * length)
        empty = length - filled
        return "▰" * filled + "▱" * empty

    @commands.command()
    async def level(self, ctx):
        user_id = ctx.author.id
        async with aiosqlite.connect("data/currency.db") as db:
            async with db.execute("SELECT xp FROM users WHERE user_id = ?", (user_id,)) as cursor:
                result = await cursor.fetchone()

        if not result:
            await ctx.send("You don't have any XP yet. Start chatting to gain XP!")
            return

        xp = result[0]
        level = self.calculate_level(xp)
        xp_current_level = self.xp_for_level(level - 1)
        xp_next_level = self.xp_for_level(level)
        xp_into_level = xp - xp_current_level
        xp_needed = xp_next_level - xp_current_level

        progress_percent = xp_into_level / xp_needed
        bar = self.generate_progress_bar(progress_percent, length=10)

        embed = discord.Embed(
            title=f"{ctx.author.display_name}'s Level",
            description=(
                f"✨ **Level:** `{level}`\n"
                f"🔹 **XP:** `{xp} / {xp_next_level}`\n"
                f"{bar} `{int(progress_percent * 100)}%`"
            ),
            color=discord.Color.purple()
        )
        embed.set_thumbnail(url=ctx.author.display_avatar.url)

        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Leveling(bot))
