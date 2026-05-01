import discord
from discord.ext import commands
import yt_dlp as youtube_dl
import asyncio

class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.queue = {}
        self.current_track = {}
        
    @commands.command(name='play', help='Play a song from YouTube')
    async def play(self, ctx, *, query: str):
        """Play a song from YouTube URL or search query"""
        if not ctx.author.voice:
            await ctx.send("You must be in a voice channel to play music.")
            return
        
        voice_channel = ctx.author.voice.channel
        voice_client = ctx.voice_client
        
        if not voice_client:
            voice_client = await voice_channel.connect()
        elif voice_client.channel != voice_channel:
            await voice_client.move_to(voice_channel)
        
        async with ctx.typing():
            ydl_opts = {
                'format': 'bestaudio/best',
                'quiet': True,
                'no_warnings': True,
            }
            
            try:
                with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(f"ytsearch:{query}", download=False)
                    url = info['entries'][0]['url']
                    title = info['entries'][0]['title']
                
                ffmpeg_opts = {
                    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
                    'options': '-vn'
                }
                
                audio_source = discord.FFmpegPCMAudio(url, **ffmpeg_opts)
                
                if not voice_client.is_playing():
                    voice_client.play(audio_source, after=lambda e: asyncio.run_coroutine_threadsafe(self.play_next(ctx), self.bot.loop).result() if e is None else None)
                    await ctx.send(f"🎵 Now playing: **{title}**")
                else:
                    if ctx.guild.id not in self.queue:
                        self.queue[ctx.guild.id] = []
                    self.queue[ctx.guild.id].append((url, title))
                    await ctx.send(f"📝 Added to queue: **{title}**")
            
            except Exception as e:
                await ctx.send(f"Error playing track: {str(e)}")
    
    async def play_next(self, ctx):
        """Play next song in queue"""
        if ctx.guild.id in self.queue and len(self.queue[ctx.guild.id]) > 0:
            url, title = self.queue[ctx.guild.id].pop(0)
            ffmpeg_opts = {
                'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
                'options': '-vn'
            }
            audio_source = discord.FFmpegPCMAudio(url, **ffmpeg_opts)
            ctx.voice_client.play(audio_source, after=lambda e: asyncio.run_coroutine_threadsafe(self.play_next(ctx), self.bot.loop).result() if e is None else None)
    
    @commands.command(name='stop', help='Stop playing music')
    async def stop(self, ctx):
        """Stop playing music and disconnect"""
        if ctx.voice_client:
            ctx.voice_client.stop()
            await ctx.voice_client.disconnect()
            if ctx.guild.id in self.queue:
                self.queue[ctx.guild.id].clear()
            await ctx.send("⏹️ Music stopped and disconnected.")
        else:
            await ctx.send("Bot is not connected to a voice channel.")
    
    @commands.command(name='pause', help='Pause the music')
    async def pause(self, ctx):
        """Pause current track"""
        if ctx.voice_client and ctx.voice_client.is_playing():
            ctx.voice_client.pause()
            await ctx.send("⏸️ Music paused.")
        else:
            await ctx.send("No music is currently playing.")
    
    @commands.command(name='resume', help='Resume the music')
    async def resume(self, ctx):
        """Resume paused track"""
        if ctx.voice_client and ctx.voice_client.is_paused():
            ctx.voice_client.resume()
            await ctx.send("▶️ Music resumed.")
        else:
            await ctx.send("No paused music to resume.")
    
    @commands.command(name='queue', help='Show the music queue')
    async def show_queue(self, ctx):
        """Display the current queue"""
        if ctx.guild.id not in self.queue or len(self.queue[ctx.guild.id]) == 0:
            await ctx.send("Queue is empty.")
        else:
            queue_list = "\n".join([f"{i+1}. {title}" for i, (_, title) in enumerate(self.queue[ctx.guild.id])])
            await ctx.send(f"📋 **Queue:**\n{queue_list}")

async def setup(bot):
    await bot.add_cog(Music(bot))
