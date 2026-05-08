import discord
from discord.ext import commands
from datetime import datetime, timedelta

from database import (
    get_last_daily,
    update_daily,
    add_xp,
    get_coins,
)
import random

def generate_daily_xp():
    roll = random.randint(1, 100)

    if roll <= 70:
        xp = random.randint(15,35)
        rarity = "Common"

    elif roll <=92:
        xp = random.randint(36,60)
        rarity = "Uncommon"

    elif roll <= 98:
        xp = random.randint(61,70)
        rarity = "Rare"

    elif roll <= 99:
        xp = random.randint(71,80)
        rarity = "Epic"

    else:
        xp = random.randint(81,90)
        rarity = "Legendary"

    return xp, rarity

def generate_daily_coins():
    roll = random.randint(1, 100)

    if roll <= 70:
        coins = random.randint(20, 40)
        rarity = "Common"
    elif roll <= 92:
        coins = random.randint(41, 70)
        rarity = "Uncommon"
    elif roll <= 98:
        coins = random.randint(71, 120)
        rarity = "Rare"
    elif roll <= 99:
        coins = random.randint(121, 180)
        rarity = "Epic"
    else:
        coins = random.randint(181, 250)
        rarity = "Legendary"
    return coins, rarity

class Daily(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def daily(self,ctx):
        user_id = ctx.author.id
        data = await get_last_daily(user_id)

        if data:
            last_claim = datetime.fromisoformat(data[0])
            now = datetime.utcnow()
            cooldown = timedelta(hours=24)
            remaining = cooldown - (now - last_claim)

            if remaining.total_seconds() > 0:
               hours = int(remaining.total_seconds() // 3600)
               minutes = int((remaining.total_seconds() % 3600) // 60)

               embed = discord.Embed(
                title="⏳ Daily Already Claimed",
                description=(
                f"You have already claimed your daily reward.\n\n"
                f"Try again in **{hours}hrs {minutes}mins**."
               ),
               color = 0xff5555
               )
               embed.set_footer(
                text="Phoenix Daily System"
               )
               return await ctx.send(embed=embed)

        xp_reward, rarity = generate_daily_xp()
        coin_reward, coin_rarity = generate_daily_coins()
        await add_xp(ctx.author.id, xp_reward)
        await add_coins(ctx.author.id, coin_reward)

        now = datetime.utcnow().isoformat()
        await update_daily(
            ctx.author.id,
            now
        )
        embed = discord.Embed(
            title="🎁 PHOENIX | DAILY REWARD",
            description=(
                f"{ctx.author.mention} claimed their daily reward.\n\n"
                f"🌟 XP Reward: **{xp_reward} XP**\n"
                f"🏆 XP Rarity: **{rarity}**"

                f"🪙 Coin Reward: **{coin_reward} XP**\n"
                f"💰 Coin Rarity: **{coin_rarity}**"
            ),
            color=0xbb86fc
        )
        if rarity == "Legendary" or coin_rarity == "Legendary":
           embed.add_field(
             name="🌌 JACKPOT",
             value="An absurdly rare reward has appeared.",
             inline=False
        )

        elif rarity == "Epic" or coin_rarity == "Epic":
           embed.add_field(
            name="🔥 ULTRA RARE",
            value="Phoenix has blessed you today.",
            inline=False
        )

        elif rarity == "Rare" or coin_rarity == "Rare":
           embed.add_field(
            name="💠 Rare Pull",
            value="Luck seems to be on your side.",
            inline=False
        )
        embed.set_footer(
            text="Phoenix Daily System ~ Rise Together. Shine Forever"
        )
        await ctx.send(embed=embed)

    @commands.command(aliases=["bal"])
    async def balance(self, ctx, member: discord.Member = None):
        member = member or ctx.author
        coins = await get_coins(member.id)
        embed = discord.Embed(
            title="💰 PHOENIX | BALANCE",
            description=(
                f"👤 User: {member.mention}\n\n"
                f"🪙 Coins: **{coins}**"
            ),
            color=0xbb86fc
        )
        embed.set_footer(
            text="Phoenix Economy System ~ Rise Together. Shine Forever"
        )
        await ctx.send(embed=embed)

async def setup(bot):
     await bot.add_cog(Daily(bot))