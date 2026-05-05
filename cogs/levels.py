import discord
from discord.ext import commands
import json
import os
from database import add_xp, get_user_data


class Levels(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.announce_channel_id = 1499481612067278958

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot or message.content.startswith("!"):
            return

        await add_xp(message.author.id, 8)
        data = await get_user_data(message.author.id)
        xp = data[0]
        lvl = data[1]

        xp_needed = lvl * 150   

        if xp >= xp_needed:

            from database import level_up
            await level_up(message.author.id)
            
            channel = self.bot.get_channel(self.announce_channel_id)
            if channel:
                embed = discord.Embed(
                    title="✨ Level Up!",
                    description=f"{message.author.mention} just reached **Level {lvl + 1}**!",
                    color=0xbb86fc
                )
                embed.set_thumbnail(url=message.author.display_avatar.url)
                embed.set_footer(text="Keep chatting to climb higher!")
                await channel.send(embed=embed)


    @commands.command(name="rank")
    async def rank(self, ctx, member: discord.Member = None):
        member = member or ctx.author
        data = await get_user_data(member.id)
        
        if data is None:
            await ctx.send("No stats found for this user.")
            return

        xp = data[0]
        lvl = data[1]
        needed = lvl * 150

        embed = discord.Embed(color=0x03dac6)
        embed.set_author(name=f"{member.name}'s Progression", icon_url=member.display_avatar.url)
        embed.add_field(name="🏆 Level", value=f"**{lvl}**", inline=True)
        embed.add_field(name="🧠 Experience", value=f"**{xp} / {needed}**", inline=True)
        
        progress = int((xp / needed) * 10)
        bar = "▰" * progress + "▱" * (10 - progress)
        embed.add_field(name="📊 Progress Bar", value=f"`{bar}`", inline=False)
        
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Levels(bot))