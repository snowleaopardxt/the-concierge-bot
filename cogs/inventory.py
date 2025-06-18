import discord
from discord.ext import commands
import aiosqlite

class Inventory(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Ensure inventory table exists
    async def create_table(self):
        async with aiosqlite.connect("data/currency.db") as db:
            await db.execute("""
                CREATE TABLE IF NOT EXISTS inventory (
                    user_id INTEGER,
                    item_name TEXT,
                    quantity INTEGER DEFAULT 0,
                    PRIMARY KEY (user_id, item_name)
                )
            """)
            await db.commit()

    @commands.Cog.listener()
    async def on_ready(self):
        await self.create_table()
        print("✅ Inventory Cog Ready")

    @commands.command()
    async def inventory(self, ctx):
        user_id = ctx.author.id
        async with aiosqlite.connect("data/currency.db") as db:
            cursor = await db.execute("SELECT item_name, quantity FROM inventory WHERE user_id = ?", (user_id,))
            rows = await cursor.fetchall()

        if not rows:
            await ctx.send("👜 Your inventory is empty.")
        else:
            embed = discord.Embed(title=f"{ctx.author.name}'s Inventory", color=0x00ffcc)
            for item, qty in rows:
                embed.add_field(name=item, value=f"Quantity: {qty}", inline=False)
            await ctx.send(embed=embed)

    @commands.command()
    async def give_item(self, ctx, member: discord.Member, item: str, quantity: int = 1):
        if quantity <= 0:
            return await ctx.send("❌ Quantity must be at least 1.")

        async with aiosqlite.connect("data/currency.db") as db:
            await db.execute("""
                INSERT INTO inventory (user_id, item_name, quantity)
                VALUES (?, ?, ?)
                ON CONFLICT(user_id, item_name) DO UPDATE SET
                    quantity = quantity + excluded.quantity
            """, (member.id, item, quantity))
            await db.commit()

        await ctx.send(f"✅ Gave {quantity}x **{item}** to {member.display_name}.")

async def setup(bot):
    await bot.add_cog(Inventory(bot))
