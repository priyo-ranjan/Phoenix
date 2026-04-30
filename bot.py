import discord
import random
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents = intents, case_insensitive=True)

@bot.event
async def on_ready():
    print(f"{bot.user} is online!")

@bot.command()
async def hello(ctx):
    await ctx.send("Hello!")

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

bot.run("MTQ5OTI1MzYxMzYzNjA5NjExMQ.GuiRP6.66Lm0J4cKB8RBPjvippjKdCiO88A0orhLoDDo4")

