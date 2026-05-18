import discord
from discord.ext import commands

from database import (
    add_coins,
    add_crates,
    remove_coins,
    remove_crates
)
class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.is_owner()
    async def givecoins(self, ctx, member: discord.Member, amount: int):
        if amount <= 0:
            return await ctx.send("Amount must be positive.")
        await add_coins(member.id, amount)
        await ctx.send(f"Gave {amount} coins to {member.mention}.")
    
    @commands.command()
    @commands.is_owner()
    async def givecrates(self, ctx, member: discord.Member, amount: int):
        if amount <= 0:
            return await ctx.send("Amount must be positive.")
        await add_crates(member.id, amount)
        await ctx.send(f"Gave {amount} crates to {member.mention}.")

async def setup(bot):
    await bot.add_cog(Admin(bot))