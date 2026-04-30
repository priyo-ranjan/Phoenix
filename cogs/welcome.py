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
       print(f"{member} has left the server.")
       channel = self.bot.get_channel(1499404085651312865)
       print(channel)

       if channel:
        
           embed = discord.Embed(
              title="💔 Member Left",
              description=f"### {member.mention} left the server.",
              color=0x2b2d31)

           embed.set_thumbnail(url=member.avatar.url)

           embed.add_field(
              name="👤 Username",
              value=member.name,
              inline=True)

           embed.add_field(
              name="🆔 ID",
              value=member.id,
              inline=True)

           embed.add_field(
              name="📉 Members Remaining",
              value=member.guild.member_count,
              inline=False)

           embed.set_footer(
              text="We hope to see them again...")

           await channel.send(embed=embed)
  
async def setup(bot):
    await bot.add_cog(Welcome(bot))
