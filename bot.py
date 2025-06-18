import discord
from discord.ext import commands
import os
import asyncio
import aiosqlite
from config import TOKEN  # Make sure your token is securely stored here
from dotenv import load_dotenv
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

# --- Bot Setup ---
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.guilds = True

bot = commands.Bot(command_prefix="!", intents=intents)


# --- Events ---
@bot.event
async def on_ready():
    print(f"✅ {bot.user} is online and ready.")

    # Ensure the database and table exist
    async with aiosqlite.connect("data/currency.db") as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                coins INTEGER DEFAULT 0,
                xp INTEGER DEFAULT 0,
                markers INTEGER DEFAULT 0
            )
        """)
        await db.commit()


# --- Commands ---
@bot.command()
@commands.is_owner()  # Only the bot owner can load cogs manually
async def load(ctx, cog):
    """Manually load a cog."""
    try:
        await bot.load_extension(f"cogs.{cog}")
        await ctx.send(f"✅ Loaded `{cog}` cog.")
    except commands.ExtensionAlreadyLoaded:
        await ctx.send(f"⚠️ `{cog}` is already loaded.")
    except commands.ExtensionNotFound:
        await ctx.send(f"❌ Cog `{cog}` not found.")
    except Exception as e:
        await ctx.send(f"❌ Failed to load `{cog}`: `{e}`")


# --- Load all cogs on startup ---
async def load_extensions():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            try:
                await bot.load_extension(f"cogs.{filename[:-3]}")
                print(f"🔁 Loaded cog: {filename}")
            except commands.ExtensionAlreadyLoaded:
                print(f"⚠️ Cog already loaded: {filename}")
            except Exception as e:
                print(f"❌ Failed to load {filename}: {e}")


# --- Main Entry Point ---
async def main():
    await load_extensions()
    await bot.start(TOKEN)


if __name__ == "__main__":
    asyncio.run(main())
