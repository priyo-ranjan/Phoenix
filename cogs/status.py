import discord
from discord.ext import commands, tasks
import random
class Status(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.statuses = [
            ("watching", "over Phoenix"),
            ("watching", "69 humans"),
            ("playing", "with the database"),
            ("listening", "server activity"),
            ("watching", "XP levels rise"),
            ("playing", "Use !help"),
            ("watching", "the inner circle"),
            ("listening", "Rise Together. Shine Forever."),
        ]
        self.rotate_status.start()

    def cog_unload(self):
        self.rotate_status.cancel()
    @tasks.loop(minutes=10)
    async def rotate_status(self):
        status_type, text = random.choice(self.statuses)

        if status_type == "playing":
            activity = discord.Game(name=text)
        elif status_type == "listening":
            activity = discord.Activity(type=discord.ActivityType.listening, name=text)
        else:
            activity = discord.Activity(type=discord.ActivityType.watching, name=text)

        await self.bot.change_presence(activity=activity)

    @rotate_status.before_loop
    async def before_status(self):
        await self.bot.wait_until_ready()
async def setup(bot):
    await bot.add_cog(Status(bot))

    