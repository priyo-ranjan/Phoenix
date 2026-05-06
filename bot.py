import discord
import random
import os
from dotenv import load_dotenv
from discord.ext import commands
from database import setup_database


load_dotenv()
TOKEN = os.getenv("TOKEN")

load_dotenv()
TOKEN = os.getenv("TOKEN")

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(
    command_prefix="!",
     intents = intents,
      case_insensitive=True,
      help_command=None
      )

@bot.event
async def on_ready():

    await setup_database()
    await bot.load_extension("cogs.commands")
    await bot.load_extension("cogs.fun")
    await bot.load_extension("cogs.moderation")
    await bot.load_extension("cogs.welcome")
    await bot.load_extension("cogs.ai")
    await bot.load_extension("cogs.levels") 
    await bot.load_extension("cogs.rep")
    await bot.load_extension("cogs.memory")
    await bot.load_extension("cogs.help")
    await bot.load_extension("cogs.leader")
    await bot.load_extension("cogs.server")
    await bot.load_extension("cogs.verify")
    await bot.load_extension("cogs.rules")
    await bot.load_extension("cogs.status")

    print(f"{bot.user} is online!")

bot.run(TOKEN)
