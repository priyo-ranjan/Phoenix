import discord
from discord.ext import commands
import json
import os

if os.path.exists("/data"):
    LEVELS_PATH = "/data/levels.json"
else:
    LEVELS_PATH = "levels.json"

class Levels(commands.Cog):
    def init(self, bot):
        self.bot = bot

    def save_levels(self, data):
        with open(LEVELS_PATH, "w") as f:
            json.dump(data, f, indent=4)

    def load_levels(self):
        try:
            if not os.path.exists(LEVELS_PATH):
                return {}
            with open(LEVELS_PATH, "r") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot or message.content.startswith("!"):
            return

        users = self.load_levels()
        user_id = str(message.author.id)

        if user_id not in users:
            users[user_id] = {"xp": 0, "level": 1}

        users[user_id]["xp"] += 5
        xp_needed = users[user_id]["level"] * 100
        
        if users[user_id]["xp"] >= xp_needed:
            users[user_id]["level"] += 1
            users[user_id]["xp"] = 0
            await message.channel.send(f"🎉 Congrats {message.author.mention}! You reached Level {users[user_id]['level']}!")

        self.save_levels(users)

    @commands.command()
    async def rank(self, ctx, member: discord.Member = None):
        member = member or ctx.author
        users = self.load_levels()
        user_id = str(member.id)

        if user_id not in users:
            await ctx.send(f"{member.display_name} hasn't earned any XP yet.")
            return

        xp = users[user_id]["xp"]
        lvl = users[user_id]["level"]
        needed = lvl * 100

        embed = discord.Embed(title=f"📊 {member.name}'s Rank", color=0x00FF00)
        embed.add_field(name="Level", value=lvl, inline=True)
        embed.add_field(name="XP", value=f"{xp}/{needed}", inline=True)
        embed.set_thumbnail(url=member.display_avatar.url)
        
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Levels(bot))