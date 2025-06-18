from discord.ext import commands
import discord
import aiosqlite
import random
from datetime import datetime, timedelta

cooldowns = {}

# 🧾 Contract definitions
CONTRACTS = {
    "cleaner": (50, 10),
    "driver": (100, 20),
    "negotiator": (200, 40),
    "tracker": (300, 60),
    "eliminator": (500, 100)
}

class Economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def ensure_user(self, db, user_id):
        await db.execute("INSERT OR IGNORE INTO users (user_id) VALUES (?)", (user_id,))
        await db.commit()

    @commands.command()
    async def balance(self, ctx):
        """Check your coin, XP and marker balance."""
        async with aiosqlite.connect("data/currency.db") as db:
            await self.ensure_user(db, ctx.author.id)
            async with db.execute("SELECT coins, xp, markers FROM users WHERE user_id = ?", (ctx.author.id,)) as cursor:
                coins, xp, markers = await cursor.fetchone()

        embed = discord.Embed(title=f"💼 Vault of {ctx.author.display_name}", color=0x2f3136)
        embed.add_field(name="💰 Coins", value=f"`{coins}`", inline=True)
        embed.add_field(name="🎯 XP", value=f"`{xp}`", inline=True)
        embed.add_field(name="🕯️ Markers", value=f"`{markers}`", inline=True)
        embed.set_thumbnail(url=ctx.author.display_avatar.url)
        await ctx.send(embed=embed)

    @commands.command()
    async def work(self, ctx):
        """Earn a small amount of coins and XP every 60 seconds."""
        user_id = ctx.author.id
        now = datetime.utcnow()

        # Cooldown: 1 minute per user
        if user_id in cooldowns and (now - cooldowns[user_id]).total_seconds() < 60:
            remaining = 60 - int((now - cooldowns[user_id]).total_seconds())
            return await ctx.send(f"🕒 You must wait `{remaining}s` before working again.")

        earnings = random.randint(20, 50)
        xp_gain = random.randint(5, 15)

        async with aiosqlite.connect("data/currency.db") as db:
            await self.ensure_user(db, user_id)
            await db.execute("UPDATE users SET coins = coins + ?, xp = xp + ? WHERE user_id = ?",
                             (earnings, xp_gain, user_id))
            await db.commit()

        cooldowns[user_id] = now
        await ctx.send(f"🔧 You completed a task and earned **{earnings} coins** and **{xp_gain} XP**!")

    @commands.command()
    async def contracts(self, ctx):
        """List available contracts and their rewards."""
        embed = discord.Embed(title="📜 Available Contracts", color=0x2f3136)
        for name, (coins, xp) in CONTRACTS.items():
            embed.add_field(name=f"🔸 {name.capitalize()}", value=f"💰 `{coins}` coins\n🎯 `{xp}` XP", inline=False)
        embed.set_footer(text="Use !accept <contract> to take one.")
        await ctx.send(embed=embed)

    @commands.command()
    async def accept(self, ctx, contract_name: str):
        """Accept and complete a contract."""
        contract_name = contract_name.lower()
        if contract_name not in CONTRACTS:
            return await ctx.send("❌ Invalid contract. Use `!contracts` to view valid ones.")

        coins, xp = CONTRACTS[contract_name]
        async with aiosqlite.connect("data/currency.db") as db:
            await self.ensure_user(db, ctx.author.id)
            await db.execute("UPDATE users SET coins = coins + ?, xp = xp + ? WHERE user_id = ?",
                             (coins, xp, ctx.author.id))
            await db.commit()

        await ctx.send(f"✅ You completed the `{contract_name}` contract and earned **{coins} coins** and **{xp} XP**!")

async def setup(bot):
    await bot.add_cog(Economy(bot))
