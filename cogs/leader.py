import discord
from discord.ext import commands
import json
import os

if os.path.exists("/data"):
    LEVELS_PATH = "/data/levels.json"
    REP_PATH = "/data/rep.json"
else:
    LEVELS_PATH = "levels.json"
    REP_PATH = "rep.json"

class Leaderboard(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def load_json(self, path):
        try:
            if not os.path.exists(path):
                return {}
            with open(path, "r") as f:
                return json.load(f)
        except:
            return {}

    @commands.command(name="top")
    async def top(self, ctx):
        levels_data = self.load_json(LEVELS_PATH)
        rep_data = self.load_json(REP_PATH).get("points", {})

        sorted_levels = sorted(levels_data.items(), key=lambda x: (x[1]['level'], x[1]['xp']), reverse=True)[:5]
        
        level_list = ""
        for i, (user_id, stats) in enumerate(sorted_levels, 1):
            user = self.bot.get_user(int(user_id))
            name = user.name if user else f"User {user_id}"
            level_list += f"**{i}.** {name} • Lvl {stats['level']}\n"

        sorted_rep = sorted(rep_data.items(), key=lambda x: x[1], reverse=True)[:5]
        
        rep_list = ""
        for i, (user_id, points) in enumerate(sorted_rep, 1):
            user = self.bot.get_user(int(user_id))
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