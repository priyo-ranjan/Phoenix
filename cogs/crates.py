import discord
from discord.ext import commands
import asyncio
import random
import aiosqlite
from database import (
    get_crates,
    add_gems,
    remove_crates,
    remove_coins,
    add_coins
)

class Crates(commands.Cog):
    def __init__(self, bot):
        self.bot = bot   
    
    @commands.command(aliases=["crate", "open"])
    async def opencrate(self, ctx, amount: int = 1):
        if amount <= 0:
            return await ctx.send(
                "📦 Amount must be positive."
            )
        crates = await get_crates(ctx.author.id)
        if crates < amount:
            return await ctx.send(
                f"📦 You only have {crates} crates."
            )
        await remove_crates(ctx.author.id, amount)
        message = await ctx.send(
            "📦 Opening crate(s)..."
        )
        await asyncio.sleep(2)

        total_coins = 0
        total_gems = 0
        total_lost = 0
        jackpots = 0

        for _ in range(amount):
            roll = random.randint(1, 100)
            if roll <= 40:
                reward = random.randint(100, 300)
                total_coins += reward
            elif roll <= 70:
                reward = random.randint(400, 800)
                total_coins += reward
            elif roll <= 90:
                gems = random.randint(1, 2)
                total_gems += gems
            elif roll <= 97:
                jackpot = random.randint(2000, 4000)
                total_coins += jackpot
                jackpots += 1
            else:
                loss = random.randint(100, 500)
                total_lost += loss

        if total_coins > 0:
            await add_coins(ctx.author.id, total_coins)
        if total_gems > 0:
            await add_gems(ctx.author.id, total_gems)
        if total_lost > 0:
            await remove_coins(ctx.author.id, total_lost)

        embed = discord.Embed(
            title=f"📦 Opening {amount} crate(s)...",
            description=(
                f"📦 Opened: {amount}\n"
                f"🪙 Coins: {total_coins}\n"
                f"💎 Gems: {total_gems}\n"
                f"💀 Lost {total_lost}\n"
                f"🔥 Jackpots: {jackpots}"
            ),
            color=discord.Color.gold()
        )
        return await message.edit(content=None, embed=embed)