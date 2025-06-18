import discord
from discord.ext import commands

class Prestige(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def prestige(self, ctx):
        await ctx.send(f"{ctx.author.mention}, you have prestiged! 🏅")

async def setup(bot):
    await bot.add_cog(Prestige(bot))
