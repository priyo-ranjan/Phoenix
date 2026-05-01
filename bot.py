import discord
import os
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()
TOKEN = os.getenv("TOKEN")

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents = intents, case_insensitive=True)

@bot.event
async def on_ready():

    await bot.load_extension("cogs.commands")
    await bot.load_extension("cogs.fun")
    await bot.load_extension("cogs.moderation")
    await bot.load_extension("cogs.welcome")
    await bot.load_extension("cogs.ai")
    await bot.load_extension("cogs.levels") 
    await bot.load_extension("cogs.rep")

    print(f"{bot.user} is online!")

bot.run(TOKEN)


