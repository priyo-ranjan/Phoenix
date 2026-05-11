import discord
from discord.ext import commands
from database import (
    has_enough_coins,
    get_coins,
    add_coins,
    remove_coins
)
import random

def generate_flip_result():
    roll = random.randint(1, 100)
    if roll <= 48:
        return "win"

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
        if result == "win":
            winnings = amount * 2
            await add_coins(
                ctx.author.id,
                winnings
            )
            return await ctx.send(f"You won the flip and received {winnings} coins")

            return await ctx.send(f"You lost {amount} coins")

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



