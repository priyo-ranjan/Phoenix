import discord
from discord.ext import commands
import random

class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def say(self, ctx, *, message: str):
        await ctx.send(message)

    @commands.command()
    async def roast(self, ctx):
        roasts = [
            "Bro fights mosquitoes and loses",
            "You got 999 pings in real life",
            "Even Windows Updates faster than your brain",
            "NPC Behaviour detected",
            "Bro has negative FPS in real life"
        ]
        await ctx.send(random.choice(roasts))

    @commands.command()
    async def hello(self, ctx):
        await ctx.send("Hello!")

async def setup(bot):
    await bot.add_cog(Fun(bot))
