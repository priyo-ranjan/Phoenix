import discord
from discord.ext import commands
from database import (
    has_enough_coins,
    get_coins,
    add_coins,
    remove_coins,
    get_gambling_data,
    update_gambling_data,
    get_crates,
    has_enough_crates,
    add_crates,
    remove_crates,
    add_gems,
    get_gems,
    add_activity_points,
    add_to_jackpot
)
import random
import asyncio
import aiosqlite

gambling_stats = {}

def generate_flip_result():
    roll = random.randint(1, 100)
    if roll <= 48:
        return "win"
    else:
        return "loss"



class Gamble(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def flip(self, ctx, amount):
        if amount.lower() == "all":
            amount = await get_coins(ctx.author.id)
            if amount <= 0:
                return await ctx.send("You have no coins to flip.")
        else:
            try:
                amount = int(amount)
            except ValueError:
                return await ctx.send("Please enter a valid amount.")

        if amount <= 0:
            return await ctx.send("Bet must be positive.")
        if not await has_enough_coins(ctx.author.id, amount):
            return await ctx.send("You do not have enough coins.")

        await remove_coins(ctx.author.id, amount)

        result = generate_flip_result()
        data = await get_gambling_data(ctx.author.id)
        fakeout = random.randint(1, 100) <= 20

        message = await ctx.send("🪙 Flipping the coin...")
        await asyncio.sleep(2)

        if result == "win":
            if fakeout:
                await message.edit(content=f"💀 You lost {amount} coins...")
                await asyncio.sleep(2)
                await message.edit(content="🔥 BLESSING OF PHOENIX ACTIVATED")
                await asyncio.sleep(1)
           
            
            data["win_streak"] += 1
            if data["win_streak"] > data["highest_streak"]:
                data["highest_streak"] = data["win_streak"]

            data["loss_streak"] = 0
            data["total_wins"] += 1
            
            multiplier = 2
            if data["win_streak"] >= 3:
                multiplier = 2.2
            if data["win_streak"] >= 5:
                multiplier = 2.5
            if data["win_streak"] >= 8:
                multiplier = 3

            winnings = int(amount * multiplier)
            if winnings > data["biggest_win"]:
                data["biggest_win"] = winnings
            
            await add_activity_points(ctx.author.id, 1)
            jackpot_tax = max(1, int(amount * 0.05))
            await add_to_jackpot(jackpot_tax)
            final_win = winnings - jackpot_tax
            await add_coins(ctx.author.id, final_win)
            await update_gambling_data(ctx.author.id, data)

            title = "🪙 Coin Flip"
            if data["win_streak"] >= 3:
                title = "🔥 Hot Streak"
            if data["win_streak"] >= 5:
                title = "⚡️ Phoenix Gambler"
            if data["win_streak"] >= 8:
                title = "👑 Casino Monster"

            embed = discord.Embed(
                title=title,
                description=(
                    f"💰 Bet: {amount} coins\n"
                    f"🌟 Result: **WIN**\n"
                    f"🪙 Received: `{final_win}` coins\n"
                    f"🏦 Jackpot Contribution: {jackpot_tax} coins\n"
                    f"🔥 Streak: `{data['win_streak']}`\n"
                ),
                color=discord.Color.green()
            )
            embed.set_footer(text=f"{ctx.author.name} is feeling lucky 🍀")

            return await message.edit(content=None, embed=embed)
        else:
            previous_streak = data["win_streak"]
            data["loss_streak"] += 1
            data["win_streak"] = 0
            data["total_losses"] += 1
            await update_gambling_data(ctx.author.id, data)

            embed = discord.Embed(
                title="💀 Coin Flip",
                description=(
                    f"💰 Bet: {amount} coins\n"
                    f"❌ Result: **LOSS**\n"
                    f"📉 Lost: `{amount}` coins\n"
                    f"💔 Streak Lost: {previous_streak}\n"
                ),
                color=discord.Color.red()
            )
            embed.set_footer(text=f"Better luck next time, {ctx.author.name}")

            return await message.edit(content=None, embed=embed)

async def setup(bot):
    await bot.add_cog(Gamble(bot))



