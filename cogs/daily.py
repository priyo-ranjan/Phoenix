import discord
from discord.ext import commands
from datetime import datetime, timedelta

from database import (
    get_last_daily,
    update_daily,
    add_xp,
    get_coins,
    add_coins,
    add_rep,
    get_gems,
    add_gems,
    get_crates,
    add_crates,
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

def generate_bonus_reward():
    bonus_roll = random.randint(1, 100)

    if bonus_roll <= 65:
        reward_type = "coins"
        amount = random.randint(10, 35)

    elif bonus_roll <= 85:
        reward_type = "rep"
        amount = 1

    elif bonus_roll <= 97:
        reward_type = "crate"
        amount = 1

    else:
        reward_type = "gems"
        amount = 1

    return reward_type, amount

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
        bonus_type, bonus_amount = generate_bonus_reward()

        await add_xp(ctx.author.id, xp_reward)
        await add_coins(ctx.author.id, coin_reward)
        if bonus_type == "coins":
            await add_coins(ctx.author.id, bonus_amount)
        elif bonus_type == "rep":
            await add_rep(ctx.author.id, bonus_amount)
        elif bonus_type == "crate":
            await add_crates(ctx.author.id, bonus_amount)
        elif bonus_type == "gems":
            await add_gems(ctx.author.id, bonus_amount)

        bonus_text = ""
        if bonus_type == "coins":
            bonus_text = f"💰 Bonus Coins: +{bonus_amount}"
        elif bonus_type == "rep":
            bonus_text = f"⭐ Bonus Rep: +{bonus_amount}"
        elif bonus_type == "crate":
            bonus_text = f"📦 Bonus Crate: {bonus_amount}"
        elif bonus_type == "gems":
            bonus_text = f"💎 Bonus Gems: {bonus_amount}"


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
                f"🏆 XP Rarity: **{rarity}**\n"                                          

                f"🪙 Coin Reward: **{coin_reward}**\n"
                f"💰 Coin Rarity: **{coin_rarity}**\n\n"

                f"{bonus_text}"
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
        embed.timestamp = datetime.utcnow()
        await ctx.send(embed=embed)


    @commands.command(aliases=["bal"])
    async def balance(self, ctx):
        member = ctx.author
        coins = await get_coins(ctx.author.id)
        gems = await get_gems(ctx.author.id)
        crates = await get_crates(ctx.author.id)
        embed = discord.Embed(
            title="💰 PHOENIX | BALANCE",
            description=(
                f"👤 User: {ctx.author.mention}\n\n"
                f"🪙 Coins: **{coins}**\n"
                f"💎 Gems: **{gems}**\n"
                f"📦 Crates: **{crates}**"
            ),
            color=0xbb86fc
        )
        embed.set_footer(
            text="Phoenix Economy System ~ Rise Together. Shine Forever"
        )
        embed.timestamp = datetime.utcnow()
        await ctx.send(embed=embed)

async def setup(bot):
     await bot.add_cog(Daily(bot))