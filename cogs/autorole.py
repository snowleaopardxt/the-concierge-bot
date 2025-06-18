import discord
from discord.ext import commands
import aiosqlite
import math

class XP(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        user_id = message.author.id
        async with aiosqlite.connect("data/currency.db") as db:
            await db.execute("""
                INSERT OR IGNORE INTO users (user_id, coins, xp, markers)
                VALUES (?, 0, 0, 0)
            """, (user_id,))

            cursor = await db.execute("SELECT xp FROM users WHERE user_id = ?", (user_id,))
            row = await cursor.fetchone()
            old_xp = row[0]
            new_xp = old_xp + 10  # XP gained per message

            old_level = int(math.sqrt(old_xp) // 10)
            new_level = int(math.sqrt(new_xp) // 10)

            await db.execute("UPDATE users SET xp = ? WHERE user_id = ?", (new_xp, user_id))
            await db.commit()

        if new_level > old_level:
            await message.channel.send(f"🎉 {message.author.mention} leveled up to **Level {new_level}**!")
            await self.assign_level_role(message.author, new_level)

    async def assign_level_role(self, member, level):
        guild = member.guild

        role_mapping = [
            (20, "High Table"),
            (10, "Cleaner"),
            (5, "Assassin"),
            (1, "Operator")
        ]

        assigned_role = None
        for lvl, role_name in role_mapping:
            if level >= lvl:
                assigned_role = discord.utils.get(guild.roles, name=role_name)
                break

        if not assigned_role:
            return

        # Remove other level roles
        level_role_names = {"Operator", "Assassin", "Cleaner", "High Table"}
        to_remove = [role for role in member.roles if role.name in level_role_names and role != assigned_role]

        try:
            if assigned_role not in member.roles:
                await member.add_roles(assigned_role, reason="Auto role assignment by level")
            if to_remove:
                await member.remove_roles(*to_remove, reason="Removing outdated level roles")
        except discord.Forbidden:
            print(f"❌ Missing permissions to manage roles for {member.display_name}")

async def setup(bot):
    await bot.add_cog(XP(bot))
