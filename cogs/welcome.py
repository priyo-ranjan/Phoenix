import discord
from discord.ext import commands

class Welcome(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        print(f"{member} has joined the server.")
        channel = self.bot.get_channel(1499402322680348797)
        print(channel)

        if channel:

            embed = discord.Embed(
              title="🌌 Another story begins!",
              description=f"Welcome {member.mention} to **{member.guild.name}**",
              color=0x5865F2)

            embed.set_thumbnail(url=member.display_avatar.url)

            embed.set_image(
              url="https://cdn.discordapp.com/attachments/1499252105947386088/1499458858643357807/LmpwZw.png?ex=69f4df62&is=69f38de2&hm=db0102eaa0c2ad5d06cb772f1fb83496af7585ce09e8192d0ae6f42d50d37caa&")

            embed.add_field(
              name="👤 Username",
              value=member.name,
              inline=True)

            embed.add_field(
              name="📈 Member Count",
              value=member.guild.member_count,
              inline=True)

            embed.add_field(
              name="🕒 Account Created",
              value=member.created_at.strftime("%d %B %Y"),
              inline=False)

            embed.set_footer(
              text="Enjoy your stay ✨")

            await channel.send(embed=embed)


    @commands.Cog.listener()
    async def on_member_remove(self, member):
       print(f"{member} has left the server.")
       channel = self.bot.get_channel(1499404085651312865)
       print(channel)

       if channel:
        
           embed = discord.Embed(
              title="💔 Member Left",
              description=f"### {member.mention} disappeared into the void...",
              color=0x1e1f22)

           embed.set_thumbnail(url=member.display_avatar.url)

           embed.set_image(url="https://cdn.discordapp.com/attachments/1499252105947386088/1499453612777279710/sad-anime-blue-monday-illustration_23-2151910258.png?ex=69f4da7f&is=69f388ff&hm=d6c57d4c65be4cc0422193b5a551ebb20e3c1664c0415e9dd093d28cac8f486d&")

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
