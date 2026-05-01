import discord
from discord.ext import commands
import json
import os
JSON_PATH = "/app/data/memory.json" if os.path.exists("/app") else "memory.json"

class Memory(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    @commands.command()
    async def remember(self, ctx, member: discord.Member, *, memory):
      try:
         with open(JSON_PATH, "r") as f:
              memories = json.load(f)
      except(FileNotFoundError, json.JSONDecodeError):
        memories = {}

      user_id = str(member.id)

      if user_id not in memories:
        memories[user_id] = []

      memories[user_id].append(memory)

      with open(JSON_PATH, "w") as f:
        json.dump(memories, f, indent=4)

      embed = discord.Embed(
        description=f"🧠 Memory saved for {member.mention}",
        color=0x5865F2
    )

      await ctx.send(embed=embed)

    @commands.command()
    async def memory(self, ctx, member: discord.Member):
        try:
            with open(JSON_PATH, "r") as f:
                memories = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            await ctx.send("No memories found.")
            return

        user_id = str(member.id)

        if user_id not in memories:
          await ctx.send("No memories found.")
          return

        memory_list = "\n".join(memories[user_id])

        embed = discord.Embed(
            title=f"🧠 Memories of {member.name}",
            description=memory_list,
            color=0x5865F2
)

        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Memory(bot))  