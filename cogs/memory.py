import discord
from discord.ext import commands
import json
import os

# --- PATH LOGIC ---
# This looks for the Volume you mounted at /data on Railway. 
# If it doesn't find it, it defaults to your local D: drive folder.
if os.path.exists("/data"):
    JSON_PATH = "/data/memory.json"
else:
    JSON_PATH = "memory.json"

class Memory(commands.Cog):
    def init(self, bot):
        self.bot = bot

    @commands.command()
    async def remember(self, ctx, member: discord.Member, *, memory):
        """Saves a memory for a specific user"""
        
        # 1. LOAD DATA (Safe way)
        try:
            if not os.path.exists(JSON_PATH):
                memories = {}
            else:
                with open(JSON_PATH, "r") as f:
                    memories = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            memories = {}

        # 2. UPDATE DATA
        user_id = str(member.id)
        if user_id not in memories:
            memories[user_id] = []
        
        memories[user_id].append(memory)

        # 3. SAVE DATA
        try:
            with open(JSON_PATH, "w") as f:
                json.dump(memories, f, indent=4)
        except Exception as e:
            await ctx.send(f"⚠️ Error saving to volume: {e}")
            return

        # 4. FEEDBACK
        embed = discord.Embed(
            description=f"🧠 Memory saved for {member.mention}",
            color=0x5865F2
        )
        await ctx.send(embed=embed)

    @commands.command()
    async def memory(self, ctx, member: discord.Member):
        """Retrieves all memories for a specific user"""
        
        # 1. LOAD DATA
        try:
            if not os.path.exists(JSON_PATH):
                await ctx.send("No memories have been created yet.")
                return
                
            with open(JSON_PATH, "r") as f:
                memories = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            await ctx.send("No memories found.")
            return

        # 2. CHECK USER
        user_id = str(member.id)
        if user_id not in memories or not memories[user_id]:
            await ctx.send(f"No memories found for {member.display_name}.")
            return

        # 3. FORMAT AND SEND
        memory_list = "\n".join([f"• {m}" for m in memories[user_id]])
        
        embed = discord.Embed(
            title=f"🧠 Memories of {member.name}",
            description=memory_list,
            color=0x5865F2
        )
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Memory(bot))