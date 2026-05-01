import discord
import os
from dotenv import load_dotenv
from discord.ext import commands
import wavelink


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
    nodes = [
        wavelink.Node(
            uri="http://node1.lavalink.trumpo.dev:80",
            password="trumpo"
        )
    ]
    await wavelink.Pool.connect(client=bot, nodes=nodes)
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
    await bot.load_extension("cogs.music")

    print(f"{bot.user} is online!")

bot.run(TOKEN)


