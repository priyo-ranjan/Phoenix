import discord
from discord.ext import commands
active_trades = {}
from database import (
    has_enough_coins,
    has_enough_gems,
    has_enough_crates
)

class Trade(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def trade(self, ctx, member: discord.Member):
        if member.bot:
            return await ctx.send("You cannot trade with bots.")
        if member.id == ctx.author.id:
            return await ctx.send("You cannot trade with yourself.")

        if ctx.author.id in active_trades:
            return await ctx.send("You are already in a trade.")
        if member.id in active_trades:
            return await ctx.send("That user is already trading.")

        active_trades[ctx.author.id] = {
            "partner": member.id,
            "coins": 0,
            "gems": 0,
            "crates": 0,
            "confirmed": False
        }
        active_traders[member.id] = {
            "partner": ctx.author.id,
            "coins": 0,
            "gems": 0,
            "crates": 0,
            "confirmed": False
        }
        await ctx.send(
            f"{member.mention}, trade request started with {ctx.author.mention}"
        )
    @commands.command()
    async def add(self, ctx, amount:int, item:str):
        if ctx.author.id not in active_trades:
            return await ctx.send("You are not in a trade.")
        item = item.lower()

        if item not in ["coins", "gems", "crates"]:
            return await ctx.send("Invalid item.")

        if amount <= 0:
            return await ctx.send("Amount must be positive.")

        if item == "coins":
            if not await has_enough_coins(ctx.author.id, amount):
                return await ctx.send("Not enough coins.")
        elif item == "gems":
            if not await has_enough_gems(ctx.author.id, amount):
                return await ctx.send("Not enough gems.")
        elif item == "crates":
            if not await has_enough_crates(ctx.author.id, amount):
                return await ctx.send("Not enough crates.")
            
        active_trades[ctx.author.id][item] = amount
        await ctx.send(
            f"{ctx.author.mention} added {amount} {item} to the trade."
        )

  
async def setup(bot):
    await bot.add_cog(Trade(bot)) 