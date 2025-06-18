import discord
from discord.ext import commands
import aiosqlite
from datetime import datetime, timedelta

class Daily(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="daily")
    async def daily(self, ctx):
        user_id = ctx.author.id
        async with aiosqlite.connect("data/currency.db") as db:
            await db.execute("""
                CREATE TABLE IF NOT EXISTS daily_timers (
                    user_id INTEGER PRIMARY KEY,
                    last_claim TEXT
                )
            """)

            cursor = await db.execute("SELECT last_claim FROM daily_timers WHERE user_id = ?", (user_id,))
            row = await cursor.fetchone()
            now = datetime.utcnow()

            if row:
                last_claim = datetime.fromisoformat(row[0])
                if now - last_claim < timedelta(hours=24):
                    next_claim = last_claim + timedelta(hours=24)
                    remaining = next_claim - now
                    await ctx.send(f"⏳ You’ve already claimed your daily reward.\nTry again in `{str(remaining).split('.')[0]}`.")
                    return

            # Give reward
            reward_coins = 100
            reward_xp = 20
            await db.execute("INSERT OR IGNORE INTO users (user_id) VALUES (?)", (user_id,))
            await db.execute("UPDATE users SET coins = coins + ?, xp = xp + ? WHERE user_id = ?", (reward_coins, reward_xp, user_id))
            await db.execute("REPLACE INTO daily_timers (user_id, last_claim) VALUES (?, ?)", (user_id, now.isoformat()))
            await db.commit()

            await ctx.send(f"🎁 You claimed your daily reward: 💰 `{reward_coins}` coins and ⭐ `{reward_xp}` XP!")

async def setup(bot):
    await bot.add_cog(Daily(bot))
