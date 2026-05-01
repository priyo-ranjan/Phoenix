import discord
from discord.ext import commands
import wavelink


class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def play(self, ctx, *, search: str):

        if not ctx.author.voice:
            await ctx.send("Join a voice channel first.")
            return

        channel = ctx.author.voice.channel

        if not ctx.voice_client:
            player = await channel.connect(cls=wavelink.Player)
        else:
            player: wavelink.Player = ctx.voice_client

        tracks = await wavelink.Playable.search(search)

        if not tracks:
            await ctx.send("No tracks found.")
            return

        track = tracks[0]

        await player.play(track)

        await ctx.send(f"Now playing: {track.title}")

    @commands.command()
    async def leave(self, ctx):

        if ctx.voice_client:
            await ctx.voice_client.disconnect()
            await ctx.send("Disconnected.")


async def setup(bot):
    await bot.add_cog(Music(bot))