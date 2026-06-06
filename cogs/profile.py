import discord
from discord.ext import commands
import asyncio
import random
from database import (
    get_gambling_data,
    update_gambling_data
)

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
        
class Profile(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def profile(self, ctx, member: discord.Member= None):
        member = member or ctx.author

        data = await get_gambling_data(member.id)

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
        embed.set_author(
            name=f"{member.name}'s Profile",
            icon_url=member.display_avatar.url
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
            text="Phoenix Profile System"
    )

        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Profile(bot))