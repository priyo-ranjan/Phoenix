import discord
from discord.ext import commands
from datetime import datetime

class Server(commands.Cog):
    def init(self, bot):
        self.bot = bot

    @commands.command(name="server", help="Shows information about the server.")
    async def server(self, ctx):

        guild = ctx.guild

        total_members = guild.member_count
        humans = len([m for m in guild.members if not m.bot])
        bots = len([m for m in guild.members if m.bot])

        text_channels = len(guild.text_channels)
        voice_channels = len(guild.voice_channels)
        categories = len(guild.categories)

        created_at = guild.created_at.strftime("%d %B %Y")

        embed = discord.Embed(
            title=f"🌌 {guild.name}",
            description=(
                "```yaml\n"
                "Welcome to The Nexus.\n"
                "A dark futuristic community powered by Phoenix.\n"
                "```"
            ),
            color=0x7b2cbf
        )

        if guild.icon:
            embed.set_thumbnail(url=guild.icon.url)

        embed.add_field(
            name="👑 Owner",
            value=f"{guild.owner}",
            inline=True
        )

        embed.add_field(
            name="🆔 Server ID",
            value=f"{guild.id}",
            inline=True
        )

        embed.add_field(
            name="📅 Created",
            value=created_at,
            inline=True
        )

        embed.add_field(
            name="👥 Members",
            value=(
                f"Total: {total_members}\n"
                f"Humans: {humans}\n"
                f"Bots: {bots}"
            ),
            inline=True
        )

        embed.add_field(
            name="💬 Channels",
            value=(
                f"Text: {text_channels}\n"
                f"Voice: {voice_channels}\n"
                f"Categories: {categories}"
            ),
            inline=True
        )

        embed.add_field(
            name="🚀 Boost Level",
            value=f"Level {guild.premium_tier}",
            inline=True
        )

        embed.add_field(
            name="✨ Roles",
            value=f"{len(guild.roles)} roles",
            inline=True
        )

        embed.add_field(
            name="🌍 Region",
            value="Automatic",
            inline=True
        )

        embed.add_field(
            name="🤖 Bot",
            value="Phoenix",
            inline=True
        )

        embed.set_image(
            url="https://images.unsplash.com/photo-1519681393784-d120267933ba"
        )

        embed.set_footer(
            text=f"Requested by {ctx.author.name}",
            icon_url=ctx.author.display_avatar.url
        )

        embed.timestamp = datetime.utcnow()

        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Server(bot))