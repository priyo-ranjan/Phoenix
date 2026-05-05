import discord
from discord.ext import commands
from database import get_top_rep, get_top_levels

class Leaderboard(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="top")
    async def top(self, ctx):
        top_levels = await get_top_levels
        top_rep = await get_top_rep()

        level_list = ""
        for i, (user_id, xp, level) in enumerate(top_levels, 1):
            user = self.bot.get_user(user_id)
            name = user.name if user else f"User {user_id}"
            level_list += f"**{i}.** {name} • Level {level}\n"

        rep_list = ""
        for i, (user_id, points) in enumerate(top_rep, 1):
            user = self.bot.get_user(user_id)
            name = user.name if user else f"User {user_id}"
            rep_list += f"**{i}.** {name} • {points} ⭐\n"

        embed = discord.Embed(title="🏆 Phoenix Server Leaderboard", color=0x00ffff)
        embed.set_thumbnail(url=ctx.guild.icon.url if ctx.guild.icon else None)
        
        embed.add_field(
            name="📈 Top Chatters (Levels)", 
            value=level_list if level_list else "No data yet", 
            inline=True
        )
        
        embed.add_field(
            name="⭐ Most Respected (Rep)", 
            value=rep_list if rep_list else "No data yet", 
            inline=True
        )
        
        embed.set_footer(text=f"Requested by {ctx.author.name}", icon_url=ctx.author.display_avatar.url)
        
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Leaderboard(bot))