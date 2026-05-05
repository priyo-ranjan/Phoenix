import discord
<<<<<<< Updated upstream
=======
import random
>>>>>>> Stashed changes
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

    print(f"{bot.user} is online!")

bot.run(TOKEN)

<<<<<<< Updated upstream
=======
@bot.command()
async def ping(ctx):
    await ctx.send("yo mf!")

@bot.command()
async def say(ctx, *, message):
    await ctx.send(message)

@bot.command()
async def roast(ctx):
    roasts = ["Bro fights mosquitoes and loses",
     "You got 999 pings in real life",
      "Even Windows Updates faster than your brain",
      "NPC Behaviour detected"]
    await ctx.send(random.choice(roasts))

bot.run(TOKEN)
>>>>>>> Stashed changes

