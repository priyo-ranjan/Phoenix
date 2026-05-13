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
    get_gems
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

def get_rank(total_wins):
    if total_wins >= 1000:
        return "👑 Casino King"
    elif total_wins >= 500:
        return "🔥 High Roller"
    elif total_wins >= 100:
        return "🎲 Gambler"
    elif total_wins >= 25:
        return "🪙 Risk Taker"
    else:
        return "☘️ Beginner"

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
           
            if amount >= 100:
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
            await update_gambling_data(ctx.author.id, data)

            await add_coins(ctx.author.id, winnings)

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
                    f"🪙 Received: `{winnings}` coins\n"
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

    @commands.command()
    @commands.is_owner()
    async def givecoins(self, ctx, member: discord.Member, amount: int):
        if amount <= 0:
            return await ctx.send("Amount must be positive.")
        await add_coins(member.id, amount)
        await ctx.send(f"Gave {amount} coins to {member.mention}.")

    @commands.command()
    async def profile(self, ctx):

        coins = await get_coins(ctx.author.id)

        data = await get_gambling_data(ctx.author.id)

        total_games = data["total_wins"] + data["total_losses"]

        if total_games == 0:
            winrate = 0
        else:
            winrate = round(
            (data["total_wins"] / total_games) * 100,
            1
        )

        rank = get_rank(data["total_wins"])

        embed = discord.Embed(
            title="👤 Phoenix Profile",
            color=discord.Color.purple()
    )

        embed.add_field(
            name="💰 Economy",
            value=(
                f"🪙 Coins: {coins}\n"
                f"💎 Gems: 0\n"
                f"📦 Crates: 0"
        ),
            inline=False
    )

        embed.add_field(
            name="🎰 Gambling Stats",
            value=(
                f"🔥 Current Streak: {data['win_streak']}\n"
                f"🏆 Highest Streak: {data['highest_streak']}\n"
                f"🌟 Total Wins: {data['total_wins']}\n"
                f"💎 Total Losses: {data['total_losses']}\n"
                f"📈 Win Rate: {winrate}%\n"
                f"💸 Biggest Win: {data['biggest_win']}"
        ),
                inline=False
    )

        embed.add_field(
            name="🎖 Rank",
            value=rank,
            inline=False
    )

        embed.set_footer(
            text="Phoenix Economy System"
    )

        await ctx.send(embed=embed)
    @commands.command()
    async def opencrate(seld, ctx):
        crates = await get_crates(ctx.author.id)
        if crates <= 0:
            return await ctx.send(
                "📦 You do not have any crates."
            )
        await remove_crates(ctx.author.id, 1)
        message = await ctx.send(
            "📦 Opening crate..."
        )
        await asyncio.sleep(2)
        roll = random.randint(1, 100)
        if roll <= 40:
            reward = random.randint(100, 300)
            await add_coins(ctx.author.id, reward)
            embed = discord.Embed(
                title="💰 Common Reward",
                description=f"You received {reward} coins.",
                color = discord.Color.green()
            )
        elif roll <= 70:
            reward = random.randint(400, 800)
            await add_coins(ctx.author.id, reward)
            embed = discord.Embed(
                title="🌟 Rare Reward",
                description=f"You received {reward} coins.",
                color = discord.Color.blue()
            )
        elif roll <= 90:
            reward = random.randint(1, 3)
            await add_gems(ctx.author.id, reward)
            embed = discord.Embed(
                title="💎 Gem drop",
                description=f"You received {gems} gems.",
                color = discord.Color.purple()
            )
        elif roll <= 97:
            jackpot = random.randint(2000, 5000)
            await add_coins(ctx.author.id, jackpot)
            embed = discord.Embed(
                title="🔥 JACKPOT",
                description=f"You have won {jackpot} coins!",
                color = discord.Color.gold()
            )
        else:
            loss = random.randint(100, 500)
            await remove_coins(ctx.author.id, loss)
            embed = discord.Embed(
                title="💀 CURSED CRATE",
                description=f"The crate stole {loss} coins.",
                color = discord.Color.red()
            )
            await message.edit(content=None, embed=embed)


async def setup(bot):
    await bot.add_cog(Gamble(bot))



