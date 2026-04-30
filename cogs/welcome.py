import discord
from discord.ext import commands

class Welcome(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = self.bot.get_channel(1499402322680348797)
        await channel.send(f"Welcome to the server, {member.mention}! We're glad to have you here.")

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        channel = self.bot.get_channel(1499404085651312865)
        await channel.send(f"{member.display_name} has left the server. We're sorry to see you go!")

async def setup(bot):
    await bot.add_cog(Welcome(bot))
