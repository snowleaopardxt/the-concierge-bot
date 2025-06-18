import discord
from discord.ext import commands
import aiosqlite

class Shop(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.items = {
            "Sword": 50,
            "Shield": 40,
            "Potion": 25,
            "Ring": 100
        }

    @commands.command()
    async def shop(self, ctx):
        embed = discord.Embed(title="🛍️ The Continental Shop", color=0xffd700)
        for item, price in self.items.items():
            embed.add_field(name=item, value=f"{price} coins", inline=False)
        await ctx.send(embed=embed)

    @commands.command()
    async def buy(self, ctx, item: str, quantity: int = 1):
        item = item.capitalize()
        if item not in self.items:
            return await ctx.send("❌ That item doesn't exist in the shop.")
        if quantity <= 0:
            return await ctx.send("❌ Quantity must be at least 1.")

        cost = self.items[item] * quantity

        async with aiosqlite.connect("data/currency.db") as db:
            cursor = await db.execute("SELECT coins FROM users WHERE user_id = ?", (ctx.author.id,))
            row = await cursor.fetchone()

            if not row or row[0] < cost:
                return await ctx.send("💸 You don't have enough coins.")

            # Deduct coins
            await db.execute("UPDATE users SET coins = coins - ? WHERE user_id = ?", (cost, ctx.author.id))

            # Add to inventory
            await db.execute("""
                INSERT INTO inventory (user_id, item_name, quantity)
                VALUES (?, ?, ?)
                ON CONFLICT(user_id, item_name) DO UPDATE SET
                    quantity = quantity + excluded.quantity
            """, (ctx.author.id, item, quantity))

            await db.commit()

        await ctx.send(f"✅ You bought {quantity}x **{item}** for {cost} coins.")

async def setup(bot):
    await bot.add_cog(Shop(bot))
