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
            await message.channel.send(
                f"🎉 {message.author.mention} leveled up to level {level + 1}!"
            )

        with open("levels.json", "w") as f:
            json.dump(users, f, indent = 4)

async def setup(bot):
    await bod.add_cog(Levels(bot))  
    


