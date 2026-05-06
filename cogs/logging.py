# logging.py

import discord
from discord.ext import commands


class Logging(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        # PUT YOUR CHANNEL IDs HERE
        self.member_log_channel = 1501684136920879104


    # MEMBER JOIN
    @commands.Cog.listener()
    async def on_member_join(self, member):

        channel = self.bot.get_channel(self.member_log_channel)

        if not channel:
            return

        embed = discord.Embed(
            title="🟢 PHOENIX | MEMBER JOINED",
            description=f"{member.mention} has entered The Nexus.",
            color=0xbb86fc
        )

        embed.add_field(
            name="👤 User",
            value=f"{member.name}",
            inline=True
        )

        embed.add_field(
            name="🆔 User ID",
            value=f"{member.id}",
            inline=True
        )

        embed.add_field(
            name="📅 Account Created",
            value=f"<t:{int(member.created_at.timestamp())}:R>",
            inline=False
        )

        embed.set_thumbnail(url=member.display_avatar.url)

        embed.set_footer(
            text="Phoenix Logging System • Rise Together. Shine Forever."
        )

        await channel.send(embed=embed)


    # MEMBER LEAVE
    @commands.Cog.listener()
    async def on_member_remove(self, member):

        channel = self.bot.get_channel(self.member_log_channel)

        if not channel:
            return

        embed = discord.Embed(
            title="🔴 PHOENIX | MEMBER LEFT",
            description=f"{member.name} has left the server.",
            color=0xbb86fc
        )

        embed.add_field(
            name="👤 User",
            value=f"{member.name}",
            inline=True
        )

        embed.add_field(
            name="🆔 User ID",
            value=f"{member.id}",
            inline=True
        )

        embed.set_thumbnail(url=member.display_avatar.url)

        embed.set_footer(
            text="Phoenix Logging System • Rise Together. Shine Forever."
        )

        await channel.send(embed=embed)
        embed = discord.Embed(
            title="✅ Member Verified",
            description=f"{member.mention} has entered the Nexus.",
            color=0x8b5cf6
)

        embed.add_field(
            name="👤 User",
            value=f"{member.name} ({member.id})",
            inline=False
)

        embed.set_thumbnail(url=member.display_avatar.url)

        embed.set_footer(text="Phoenix Logging System")
        await log_channel.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Logging(bot))