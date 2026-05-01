import discord
from discord.ext import commands
import yt_dlp
import asyncio

class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
        self.YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': 'True'}
        
        self.FFMPEG_OPTIONS = {
            'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
            'options': '-vn'
        }

    @commands.command()
    async def play(self, ctx, *, url):
        """Joins voice and plays from a YouTube URL"""
        if ctx.author.voice is None:
            return await ctx.send("You need to be in a voice channel!")
        
        voice_channel = ctx.author.voice.channel
        if ctx.voice_client is None:
            await voice_channel.connect()
        else:
            await ctx.voice_client.move_to(voice_channel)

        async with ctx.typing():
            with yt_dlp.YoutubeDL(self.YDL_OPTIONS) as ydl:
                info = ydl.extract_info(f"ytsearch:{url}", download=False)
                if 'entries' in info:
                    info = info['entries'][0]
                url2 = info['url']
                title = info['title']
                
                source = await discord.FFmpegOpusAudio.from_probe(url2, **self.FFMPEG_OPTIONS)
                ctx.voice_client.play(source)
                
        await ctx.send(f"Now playing: {title}")

    @commands.command()
    async def stop(self, ctx):
        """Stops music and leaves the channel"""
        if ctx.voice_client:
            await ctx.voice_client.disconnect()
            await ctx.send("Disconnected.")
        else:
            await ctx.send("I'm not in a voice channel.")

async def setup(bot):
    await bot.add_cog(Music(bot))