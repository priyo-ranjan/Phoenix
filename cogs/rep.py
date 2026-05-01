import discord
from discord.ext import commands
import json
import os

if os.path.exists("/data"):
    PATH = "/data/rep.json"
else:
    PATH = "rep.json"

class Reputation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def get_data(self):
        try:
            if not os.path.exists(PATH):
                return {}
            with open(PATH, "r") as f:
                return json.load(f)
        except:
            return {}

    def save_data(self, data):
        with open(PATH, "w") as f:
            json.dump(data, f, indent=4)

    @commands.command(name="rep")
    async def rep(self, ctx, member: discord.Member):
        if member.id == ctx.author.id:
            await ctx.send("❌ You cannot give reputation to yourself!")
            return

        if member.bot:
            await ctx.send("❌ You cannot give reputation to a bot!")
            return

        data = self.get_data()
        user_id = str(member.id)

        if user_id not in data:
            data[user_id] = 0
        
        data[user_id] += 1
        self.save_data(data)

        embed = discord.Embed(
            description=f"⭐ {ctx.author.mention} has given a reputation point to {member.mention}!",
            color=0xFFD700
        )
        await ctx.send(embed=embed)

    @commands.command(name="reps")
    async def reps(self, ctx, member: discord.Member = None):
        member = member or ctx.author
        data = self.get_data()
        user_id = str(member.id)
        
        points = data.get(user_id, 0)

        embed = discord.Embed(title="🏆 Reputation Stats", color=0xFFD700)
        embed.set_thumbnail(url=member.display_avatar.url)
        embed.add_field(name="User", value=member.mention, inline=True)
        embed.add_field(name="Total Rep", value=f"**{points}** Points", inline=True)
        embed.set_footer(text="Give rep to others using !rep @user")
        
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Reputation(bot))s