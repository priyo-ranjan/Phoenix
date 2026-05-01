import discord
from discord.ext import commands
import json
import os
import time

if os.path.exists("/data"):
    PATH = "/data/rep.json"
else:
    PATH = "rep.json"

class Reputation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def get_all_data(self):
        try:
            if not os.path.exists(PATH):
                return {"points": {}, "cooldowns": {}}
            with open(PATH, "r") as f:
                return json.load(f)
        except:
            return {"points": {}, "cooldowns": {}}

    def save_all_data(self, data):
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

        data = self.get_all_data()
        author_id = str(ctx.author.id)
        target_id = str(member.id)
        current_time = time.time()

        last_rep_time = data["cooldowns"].get(author_id, 0)
        cooldown_seconds = 86400 # 24 hours

        if current_time - last_rep_time < cooldown_seconds:
            remaining = int((last_rep_time + cooldown_seconds) - current_time)
            hours = remaining // 3600
            minutes = (remaining % 3600) // 60
            await ctx.send(f"⏳ You can give rep again in **{hours}h {minutes}m**.")
            return

        if target_id not in data["points"]:
            data["points"][target_id] = 0
        
        data["points"][target_id] += 1
        data["cooldowns"][author_id] = current_time
        
        self.save_all_data(data)

        embed = discord.Embed(
            description=f"⭐ {ctx.author.mention} has given a reputation point to {member.mention}!",
            color=0xFFD700
        )
        await ctx.send(embed=embed)

    @commands.command(name="reps")
    async def reps(self, ctx, member: discord.Member = None):
        member = member or ctx.author
        data = self.get_all_data()
        user_id = str(member.id)
        
        points = data["points"].get(user_id, 0)

        embed = discord.Embed(title="🏆 Reputation Stats", color=0xFFD700)
        embed.set_thumbnail(url=member.display_avatar.url)
        embed.add_field(name="User", value=member.mention, inline=True)
        embed.add_field(name="Total Rep", value=f"**{points}** Points", inline=True)
        embed.set_footer(text="You can give 1 rep every 24 hours!")
        
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Reputation(bot))