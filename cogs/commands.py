import discord
from discord.ext import commands

class Commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ping(self, ctx):
      await ctx.send("yo")

    @commands.command()
    async def userinfo(self, ctx, member: discord.Member = None):

     if member is None:
        member = ctx.author

     embed = discord.Embed(
        title=f"{member.name}'s Info",
        color=discord.Color.green()
    )
     embed.set_thumbnail(url=member.avatar.url)
     embed.add_field(
        name="Username",
        value=member.name,
        inline=False
    )
     embed.add_field(
        name="Display Name",
        value=member.display_name,
        inline=False
    )
     embed.add_field(
        name="User ID",
        value=member.id,
        inline=False
    )
     embed.add_field(
        name="Account Created",
        value=member.created_at.strftime("%d %B %Y"),
        inline=False
    )
     embed.add_field(
        name="Joined Server",
        value=member.joined_at.strftime("%d %B %Y"),
        inline=False
    )
     await ctx.send(embed=embed)

    @commands.command()
    async def info(self,ctx):

     embed = discord.Embed(title = "Phoenix", description = "My first Discord Bot made with python", color = discord.Color.red())
     embed.add_field(name = "Creator", value = "Priyo Ranjan", inline = False)
     embed.add_field(name = "Language", value = "Python", inline = False)
     embed.add_field(name = "Library", value = "discord.py", inline = False)
     embed.set_footer(text = "Powered by Priyo")
     embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1499252105947386088/1499362774000730132/2b.webp?ex=69f485e6&is=69f33466&hm=be05a27627beb3f807aedef1383a0ffd712cf3e8a84e771e0c224e6f4554f662&")
     await ctx.send(embed = embed)

async def setup(bot):
    await bot.add_cog(Commands(bot))

