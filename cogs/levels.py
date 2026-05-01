import discord
from discord.ext import commands
import json
import os

if os.path.exists("/data"):
    PATH = "/data/levels.json"
else:
    PATH = "levels.json"

class Levels(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.announce_channel_id = 1499481612067278958

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

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot or message.content.startswith("!"):
            return

        data = self.get_data()
        user_id = str(message.author.id)

        if user_id not in data:
            data[user_id] = {"xp": 0, "level": 1}

        data[user_id]["xp"] += 8
        lvl = data[user_id]["level"]
        xp_needed = lvl * 150

        if data[user_id]["xp"] >= xp_needed:
            data[user_id]["level"] += 1
            data[user_id]["xp"] = 0
            
            channel = self.bot.get_channel(self.announce_channel_id)
            if channel:
                embed = discord.Embed(
                    title="✨ Level Up!",
                    description=f"{message.author.mention} just reached **Level {lvl + 1}**!",
                    color=0xbb86fc
                )
                embed.set_thumbnail(url=message.author.display_avatar.url)
                embed.set_footer(text="Keep chatting to climb higher!")
                await channel.send(embed=embed)

        self.save_data(data)

    @commands.command(name="rank")
    async def rank(self, ctx, member: discord.Member = None):
        member = member or ctx.author
        data = self.get_data()
        user_id = str(member.id)

        if user_id not in data:
            await ctx.send("No stats found for this user.")
            return

        xp = data[user_id]["xp"]
        lvl = data[user_id]["level"]
        needed = lvl * 150

        embed = discord.Embed(color=0x03dac6)
        embed.set_author(name=f"{member.name}'s Progression", icon_url=member.display_avatar.url)
        embed.add_field(name="🏆 Level", value=f"**{lvl}**", inline=True)
        embed.add_field(name="🧠 Experience", value=f"**{xp} / {needed}**", inline=True)
        
        progress = int((xp / needed) * 10)
        bar = "▰" * progress + "▱" * (10 - progress)
        embed.add_field(name="📊 Progress Bar", value=f"`{bar}`", inline=False)
        
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Levels(bot))