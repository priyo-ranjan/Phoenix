import discord
from discord.ext import commands
import yt_dlp
import asyncio

ytdl_format_options = {
    'format': 'bestaudio',
    'noplaylist': True,
    'quiet': True,
    'default_search': 'ytsearch',
    'source address': '0.0.0.0',
    'cookiefile': 'cookies.txt'
}

ffmpeg_options = {
    'options': '-vn'
}

ytdl = yt_dlp.YoutubeDL(ytdl_format_options)


class YTDLSource(discord.PCMVolumeTransformer):

    def init(self, source, *, data, volume=0.5):
        super().init(source, volume)

        self.data = data
        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=True):

        loop = loop or asyncio.get_event_loop()

        data = await loop.run_in_executor(
            None,
            lambda: ytdl.extract_info(url, download=not stream)
        )

        if 'entries' in data:
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)

        return cls(
            discord.FFmpegPCMAudio(filename, executable="ffmpeg", **ffmpeg_options),
            data=data
        )


class Music(commands.Cog):

    def init(self, bot):
        self.bot = bot

    @commands.command()
    async def play(self, ctx, *, search):

        if not ctx.author.voice:
            await ctx.send("Join a VC first.")
            return

        channel = ctx.author.voice.channel

        if ctx.voice_client is None:
            vc = await channel.connect()
        else:
            vc = ctx.voice_client

        async with ctx.typing():

            player = await YTDLSource.from_url(
                search,
                loop=asyncio.get_event_loop(),
                stream=True
            )

            vc.play(
                player,
                after=lambda e: print(f'Player error: {e}') if e else None
            )

        await ctx.send(f"🎵 Now playing: {player.title}")

    @commands.command()
    async def pause(self, ctx):
        if ctx.voice_client:
            ctx.voice_client.pause()
            await ctx.send("Paused ⏸️")

    @commands.command()
    async def resume(self, ctx):
        if ctx.voice_client:
            ctx.voice_client.resume()
            await ctx.send("Resumed ▶️")

    @commands.command()
    async def skip(self, ctx):
        if ctx.voice_client:
            ctx.voice_client.stop()
            await ctx.send("Skipped ⏭️")

    @commands.command()
    async def leave(self, ctx):
        if ctx.voice_client:
            await ctx.voice_client.disconnect()
            await ctx.send("Left VC 👋")


async def setup(bot):
    await bot.add_cog(Music(bot))