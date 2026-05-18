import discord
from discord.ext import commands
import asyncio
import random
from database import (
    get_coins,
    get_gems,
    get_crates,
    get_gambling_data
)

class Profile(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def profile(self, ctx):

        coins = await get_coins(ctx.author.id)
        gems = await get_gems(ctx.author.id)
        crates = await get_crates(ctx.author.id)

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
                f"💎 Gems: {gems}\n"
                f"📦 Crates: {crates}"
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
