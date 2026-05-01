import discord
from discord.ext import commands
import yt_dlp
import asyncio

class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
        self.YDL_OPTIONS = {
            'format': 'bestaudio/best',
            'noplaylist': True,
            'quiet': True,
            'no_warnings': True,
            'default_search': 'scsearch',
            'source_address': '0.0.0.0'
        }
        
        self.FFMPEG_OPTIONS = {
            'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
            'options': '-vn'
        }

    @commands.command()
    async def play(self, ctx, *, url):
        if ctx.author.voice is None:
            return await ctx.send("You need to be in a voice channel!")
        
        voice_channel = ctx.author.voice.channel
        if ctx.voice_client is None:
            await voice_channel.connect()
        else:
            await ctx.voice_client.move_to(voice_channel)

        async with ctx.typing():
            try:
                # This now searches SoundCloud instead of YouTube
                search_query = url if url.startswith('http') else f"scsearch:{url}"
                
                with yt_dlp.YoutubeDL(self.YDL_OPTIONS) as ydl:
                    info = ydl.extract_info(search_query, download=False)
                    if 'entries' in info:
                        info = info['entries'][0]
                    url2 = info['url']
                    title = info['title']
                
                source = await discord.FFmpegOpusAudio.from_probe(url2, **self.FFMPEG_OPTIONS)
                ctx.voice_client.play(source)
                await ctx.send(f"Now playing (SoundCloud): {title}")
            except Exception as e:
                await ctx.send(f"Error: {e}")

    @commands.command()
    async def stop(self, ctx):
        if ctx.voice_client:
            await ctx.voice_client.disconnect()
            await ctx.send("Disconnected.")
        else:
            await ctx.send("I'm not in a voice channel.")

    @commands.command()
    async def pause(self, ctx):
        if ctx.voice_client and ctx.voice_client.is_playing():
            ctx.voice_client.pause()
            await ctx.send("Paused ⏸️")
        else:
            await ctx.send("Nothing is playing right now.")

    @commands.command()
    async def resume(self, ctx):
        if ctx.voice_client and ctx.voice_client.is_paused():
            ctx.voice_client.resume()
            await ctx.send("Resumed ▶️")
        else:
            await ctx.send("The music isn't paused.")

    @commands.command()
    async def skip(self, ctx):
        if ctx.voice_client and (ctx.voice_client.is_playing() or ctx.voice_client.is_paused()):
            ctx.voice_client.stop()
            await ctx.send("Skipped ⏭️")
        else:
            await ctx.send("Nothing is playing to skip.")

    @commands.command()
    async def disconnect(self, ctx):
        if ctx.voice_client:
            await ctx.voice_client.disconnect()
            await ctx.send("Leaving the voice channel. 👋")
        else:
            await ctx.send("I'm not in a voice channel.")

async def setup(bot):
    await bot.add_cog(Music(bot))