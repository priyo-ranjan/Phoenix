import discord
from discord.ext import commands
import time
from database import add_rep, get_rep, get_last_rep, update_rep_cooldown
from datetime import datetime, timedelta

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
        data = await get_last_rep(author_id)

        if data:
            last_rep_time = datetime.fromisoformat(data[0])
            now = datetime.utcnow()

            cooldown = timedelta(hours=24)
            remaining = cooldown - (now - last_rep_time)

            if remaining.total_seconds() > 0:
                hours = int(remaining.total_seconds() // 3600)
                minutes = int((remaining.total_seconds() % 3600) // 60)

                await ctx.send(
            f"⏳ You can give rep again in {hours}h {minutes}m."
        )
                return

        await add_rep(member.id)
        now = datetime.utcnow().isoformat()
        await update_rep_cooldown(author_id, now)
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