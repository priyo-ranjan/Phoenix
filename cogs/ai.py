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
            {
                "role": "system", 
                "content": ("You are a funny, sarcastic, chill Discord AI Assistant."
                "You act like a close online friend with gen Z humor."
                "You lightly roast users in a playful way, use meme humor naturally."
                "Keep responses entertaining, witty, short to medium length."
                "Keep responses concise and under 1950 words. If the response exceeds this limit, truncate it and dont leave unfinished sentences")},
            {
                "role": "user", "content": prompt
                }
        ],
        temperature=0.9,
        max_tokens=500
    )
        reply = response.choices[0].message.content

        if len(reply) > 2000:
            reply = reply[:1990] + "..."
        await ctx.send(reply)

async def setup(bot):
    await bot.add_cog(AI(bot))

