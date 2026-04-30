import discord
from discord.ext import commands
from groq import Groq
import os

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

class AI(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ai(self, ctx, *, prompt):
        response = client.chat.completions.create(
          model="llama-3.3-70b-versatile",
          messages=[
            {"role": "user", "content": prompt}
        ]
    )
        await ctx.send(response.choices[0].message.content)

async def setup(bot):
    await bot.add_cog(AI(bot))

