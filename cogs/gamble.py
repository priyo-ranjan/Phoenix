import discord
from discord.ext import commands
from database import (
    has_enough_coins,
    get_coins,
    add_coins,
    remove_coins
)
import random
import asyncio

def generate_flip_result():
    roll = random.randint(1, 100)
    if roll <= 48:
        return "win"
    else:
        return "loss"
    

class Gamble(commands.Cog):
    def __init__(self,bot):
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
        fakeout = random.randint(1, 100) <= 20

        message = await ctx.send("🪙 Flipping the coin...")
        await asyncio.sleep(2)
            
        if result == "win":
            if fakeout:
              await message.edit(
                content=f"💀 You lost `{amount}` coins..."
                )
              await asyncio.sleep(2)
              await message.edit(
                content="🔥 PHOENIX BLESSING ACTIVATED"
                )
              await asyncio.sleep(1)
            winnings = amount * 2
            await add_coins(
                ctx.author.id,
                winnings
            )
            
            embed = discord.Embed(
              title="🎲 Coin Flip",
              description=(
                f"💰 Bet: `{amount}` coins\n"
                f"🌟 Result: **WIN**\n"
                f"🪙 Received: `{winnings}` coins"
            ),
              color = discord.Color.green()
        )
            embed.set_footer(
              text= f"{ctx.author.name} is feeling lucky 🍀"
        )
            return await message.edit(
                content=None,
                embed=embed
            )

        else:
            embed = discord.Embed(
              title="🎲 Coin Flip",
              description=(
                f"💰 Bet: `{amount}` coins\n"
                f"💀 Result: **LOSS**\n"
                f"🪙 LOST: `{amount}` coins"
            ),
              color = discord.Color.red()
        )
            embed.set_footer(
              text= f"Better luck next time, {ctx.author.name}"
        )
            return await message.edit(
                content=None,
                embed=embed
            )
            

    @commands.command()
    @commands.is_owner()
    async def givecoins(self, ctx, member : discord.Member, amount: int):
        if amount <= 0:
            return await ctx.send("Amount must be positive.")
        await add_coins(member.id, amount)
        await ctx.send(f"Gave {amount} coins to {member.mention}."
        )
async def setup(bot):
    await bot.add_cog(Gamble(bot))



