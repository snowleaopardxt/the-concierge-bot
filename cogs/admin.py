from discord.ext import commands

class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ping(self, ctx):
        await ctx.send("Pong!")

# ✅ Required setup function for dynamic loading
async def setup(bot):
    await bot.add_cog(Admin(bot))
