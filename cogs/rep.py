import discord
from discord.ext import commands
import time
from database import add_rep, get_rep

class Reputation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="rep")
    async def rep(self, ctx, member: discord.Member):
        if member.id == ctx.author.id:
            await ctx.send("❌ You cannot give reputation to yourself!")
            return

        if member.bot:
            await ctx.send("❌ You cannot give reputation to a bot!")
            return

        current_time = time.time()
        author_id = str(ctx.author.id)
        if not hasattr(self, "cooldowns"):
            self.cooldowns = {}
        last_rep_time = self.cooldowns.get(author_id, 0)

        cooldown_seconds = 86400 # 24 hours

        if current_time - last_rep_time < cooldown_seconds:
            remaining = int((last_rep_time + cooldown_seconds) - current_time)
            hours = remaining // 3600
            minutes = (remaining % 3600) // 60
            await ctx.send(f"⏳ You can give rep again in **{hours}h {minutes}m**.")
            return

        await add_rep(member.id)
        self.cooldowns[author_id] = current_time

        embed = discord.Embed(
            description=f"⭐ {ctx.author.mention} has given a reputation point to {member.mention}!",
            color=0xFFD700
        )
        await ctx.send(embed=embed)

    @commands.command(name="reps")
    async def reps(self, ctx, member: discord.Member = None):
        member = member or ctx.author
        
        points = await get_rep(member.id)
        embed = discord.Embed(title="🏆 Reputation Stats", color=0xFFD700)
        embed.set_thumbnail(url=member.display_avatar.url)
        embed.add_field(name="User", value=member.mention, inline=True)
        embed.add_field(name="Total Rep", value=f"**{points}** Points", inline=True)
        embed.set_footer(text="You can give 1 rep every 24 hours!")
        
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Reputation(bot))