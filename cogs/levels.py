import discord
from discord.ext import commands
import json
import random

class Levels(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        with open("levels.json", "r") as f:
           users = json.load(f)
           
        user_id = str(message.author.id)

        if user_id not in users:
            users[user_id] = {
                "xp": 0,
                "level": 1
            }
        xp_gain = random.randint(5, 15)
        users[user_id]["xp"] += xp_gain

        xp = users[user_id]["xp"]
        level = users[user_id]["level"]

        if xp >= level * 100:
            users[user_id]["level"] += 1
            level_channel = self.bot.get_channel(1499481612067278958)

            if level_channel:
                embed = discord.Embed(
                    title="💫Level up!",
                    description=f"Congratulations 🎉 {message.author.mention}, you have reached **Level {level + 1}!**",
                    color=0x5865F2
                )
                embed.add_field(
                    name="Current XP",
                    value=users[user_id]["xp"],
                    inline=True
                )
                embed.set_footer(
                    text="Keep chatting to gain more XP 💫"
                )
                                   
                await level_channel.send(embed=embed)

        with open("levels.json", "w") as f:
            json.dump(users, f, indent = 4)

async def setup(bot):
    await bot.add_cog(Levels(bot))  



