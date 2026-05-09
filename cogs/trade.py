import discord
from discord.ext import commands
from database import (
    has_enough_coins,
    has_enough_gems,
    has_enough_crates
)
active_trades = {}

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
            "confirmed": []
        }
        active_trades[member.id] = {
            "partner": ctx.author.id,
            "coins": 0,
            "gems": 0,
            "crates": 0,
            "confirmed": []
        }
        await ctx.send(
            f"{member.mention}, trade request started with {ctx.author.mention}"
        )
    @commands.command(name="offer")
    async def offer(self, ctx, amount:int, item:str):
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

    @commands.command()
    async def remove(self, ctx, item:str):
        if ctx.author.id not in active_trades:
            return await ctx.send("You are not in a trade.")
        item = item.lower()

        if item not in ["coins", "crates", "gems"]:
            return await ctx.send("Invalit item.")
        active_trades[ctx.author.id][item] = 0
        await ctx.send(
            f"{ctx.author.mention} removed {item} from the trade."
        )
    
    @commands.command()
    async def confirm(self, ctx):
        if ctx.author.id not in active_trades:
            return await ctx.send("You are not in a trade.")
        trade = active_trades[ctx.author.id]
        partner_id = trade["partner"]

        if ctx.author.id not in trade["confirmed"]:
            trade["confirmed"].append(ctx.author.id)
        await ctx.send(
            f"{ctx.author.mention} confirmed the trade."
        )
        partner_trade = active_trades[partner_id]
        if(
            ctx.author.id in trade["confirmed"]
            and partner_id in partner_trade["confirmed"]
        ):
            await ctx.send("Trade Completed.")

    @commands.command()
    async def cancel(self, ctx):
        if ctx.author.id not in active_trades:
            return await ctx.send("You are not in a trade.")
        partner_id = active_trades[ctx.author.id]["partner"]
        del active_trades[ctx.author.id]
        if partner_id in active_trades:
            del active_trades[partner_id]
        await ctx.send("Trade cancelled")

async def setup(bot):
    await bot.add_cog(Trade(bot)) 