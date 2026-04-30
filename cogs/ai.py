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
            {"role": "system", "content": "Keep responses concise and under 1950 words. If the response exceeds this limit, truncate it and dont leave unfinished sentences"},
            {"role": "user", "content": prompt}
        ]
    )
        reply = response.choices[0].message.content

        if len(reply) > 2000:
            reply = reply[:1990] + "..."
        await ctx.send(reply)

async def setup(bot):
    await bot.add_cog(AI(bot))

