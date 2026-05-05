import discord
from discord.ext import commands

from database import add_memory, get_memory, delete_memory
from database import get_all_memories


class Memory(commands.Cog):

    def init(self, bot):
        self.bot = bot

    @commands.command(name="memories")
    async def memories(self, ctx):
      memories = await get_all_memories(ctx.author.id)

      embed = discord.Embed(
        title="🧠 Your Memories",
        color=0x00ffff
    )

      if not memories:
        embed.description = "No memories saved yet."
      else:
        text = ""
        for key, value in memories:
            text += f"🔑 {key} → {value}\n"

        embed.description = text

    embed.set_thumbnail(url=ctx.author.display_avatar.url)
    embed.set_footer(
        text=f"Requested by {ctx.author.name}",
        icon_url=ctx.author.display_avatar.url
    )

    await ctx.send(embed=embed)

    @commands.command(name="remember")
    async def remember(self, ctx, key=None, *, value=None):

        if key is None or value is None:
            embed = discord.Embed(
                title="🧠 Memory System",
                description=(
                    "Store something permanently in Phoenix's memory.\n\n"
                    "Usage:\n"
                    "!remember <key> <value>\n\n"
                    "Example:\n"
                    "!remember favorite_game Wuthering Waves"
                ),
                color=0x00ffff
            )

            embed.set_footer(
                text=f"Requested by {ctx.author.name}",
                icon_url=ctx.author.display_avatar.url
            )

            return await ctx.send(embed=embed)

        key = key.lower()

        await add_memory(ctx.author.id, key, value)

        embed = discord.Embed(
            title="🧠 Memory Saved",
            description=(
                f"Successfully stored memory for {ctx.author.mention}\n\n"
                f"🔑 Key: {key}\n"
                f"💭 Value: {value}"
            ),
            color=0x00ffcc
        )

        embed.set_thumbnail(url=ctx.author.display_avatar.url)

        embed.set_footer(
            text="Phoenix Memory System",
            icon_url=ctx.guild.icon.url if ctx.guild.icon else None
        )

        await ctx.send(embed=embed)


    @commands.command(name="memory")
    async def memory(self, ctx, key=None):

        if key is None:

            embed = discord.Embed(
                title="🧠 Memory Lookup",
                description=(
                    "Usage:\n"
                    "!memory <key>\n\n"
                    "Example:\n"
                    "!memory favorite_game"
                ),
                color=0x00ffff
            )

            embed.set_footer(
                text=f"Requested by {ctx.author.name}",
                icon_url=ctx.author.display_avatar.url
            )

            return await ctx.send(embed=embed)

        key = key.lower()

        value = await get_memory(ctx.author.id, key)

        if value is None:

            embed = discord.Embed(
                title="❌ Memory Not Found",
                description=(
                    f"No memory stored for key:\n"
                    f"{key}"
                ),
                color=0xff4d4d
            )

            embed.set_thumbnail(url=ctx.author.display_avatar.url)

            return await ctx.send(embed=embed)

        embed = discord.Embed(
            title="🧠 Memory Retrieved",
            color=0x00ffff
        )

        embed.add_field(
            name="🔑 Key",
            value=f"{key}",
            inline=False
        )

        embed.add_field(
            name="💭 Stored Value",
            value=value,
            inline=False
        )

        embed.set_thumbnail(url=ctx.author.display_avatar.url)

        embed.set_footer(
            text=f"Requested by {ctx.author.name}",
            icon_url=ctx.author.display_avatar.url
        )

        await ctx.send(embed=embed)


    @commands.command(name="forget")
    async def forget(self, ctx, key=None):

        if key is None:

            embed = discord.Embed(
                title="🗑️ Forget Memory",
                description=(
                    "Usage:\n"
                    "!forget <key>\n\n"
                    "Example:\n"
                    "!forget favorite_game"
                ),
                color=0xffcc00
            )

            embed.set_footer(
                text=f"Requested by {ctx.author.name}",
                icon_url=ctx.author.display_avatar.url
            )

            return await ctx.send(embed=embed)

        key = key.lower()

        value = await get_memory(ctx.author.id, key)

        if value is None:

            embed = discord.Embed(
                title="❌ Memory Not Found",
                description=f"There is no saved memory for {key}",
                color=0xff4d4d
            )

            return await ctx.send(embed=embed)

        await delete_memory(ctx.author.id, key)

        embed = discord.Embed(
            title="🗑️ Memory Deleted",
            description=(
                f"Phoenix has forgotten:\n\n"
                f"🔑 {key}"
            ),
            color=0xff5555
        )

        embed.set_thumbnail(url=ctx.author.display_avatar.url)

        embed.set_footer(
            text="Memory successfully removed",
            icon_url=ctx.author.display_avatar.url
        )

        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Memory(bot))