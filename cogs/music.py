import discord
from discord.ext import commands
import yt_dlp
import asyncio
import subprocess
import shutil

class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.queue = []
        self.current = None
        self.is_playing = False
        
        # yt-dlp options for SoundCloud (no ffmpeg needed)
        self.ydl_options = {
            'format': 'bestaudio/best',
            'noplaylist': True,
            'default_search': 'scsearch',
            'quiet': False,
            'no_warnings': False,
            'socket_timeout': 30,
        }

    @commands.command(name='play', help='Play a song from SoundCloud')
    async def play(self, ctx, *, search):
        """Play a song from SoundCloud"""
        async with ctx.typing():
            try:
                # Search on SoundCloud
                with yt_dlp.YoutubeDL(self.ydl_options) as ydl:
                    info = ydl.extract_info(f"scsearch:{search}", download=False)
                    
                if not info or 'entries' not in info or len(info['entries']) == 0:
                    await ctx.send("❌ No results found on SoundCloud.")
                    return
                
                video = info['entries'][0]
                url = video['url']
                title = video['title']
                
                # Add to queue
                song_info = {
                    'url': url,
                    'title': title,
                    'requester': ctx.author
                }
                self.queue.append(song_info)
                
                await ctx.send(f"✅ Added to queue: **{title}**")
                
                # Start playing if not already playing
                if not self.is_playing:
                    await self._play_next(ctx)
                    
            except Exception as e:
                await ctx.send(f"❌ Error: {str(e)}")

    async def _play_next(self, ctx):
        """Play the next song in queue"""
        if not self.queue:
            self.is_playing = False
            self.current = None
            return
        
        self.is_playing = True
        self.current = self.queue.pop(0)
        
        try:
            # Create audio source using yt-dlp with pipe approach
            with yt_dlp.YoutubeDL(self.ydl_options) as ydl:
                info = ydl.extract_info(self.current['url'], download=False)
                audio_url = info.get('url')
            
            # Create FFmpeg audio source (works on Railway without ffmpeg binary issues)
            source = discord.PCMVolumeTransformer(
                discord.FFmpegPCMAudio(
                    audio_url,
                    before_options="-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5",
                    options="-vn"
                )
            )
            
            voice_client = ctx.voice_client
            
            def after_play(error):
                if error:
                    print(f"Player error: {error}")
                asyncio.run_coroutine_threadsafe(self._play_next(ctx), self.bot.loop)
            
            voice_client.play(source, after=after_play)
            
            # Announce the song
            embed = discord.Embed(
                title="🎵 Now Playing",
                description=self.current['title'],
                color=discord.Color.blurple()
            )
            embed.set_footer(text=f"Requested by {self.current['requester']}")
            await ctx.send(embed=embed)
            
        except Exception as e:
            await ctx.send(f"❌ Error playing song: {str(e)}")
            await self._play_next(ctx)

    @commands.command(name='resume', help='Resume the current song')
    async def resume(self, ctx):
        """Resume the current song"""
        if not ctx.voice_client:
            await ctx.send("❌ Not connected to a voice channel.")
            return
        
        if ctx.voice_client.is_paused():
            ctx.voice_client.resume()
            await ctx.send("▶️ Resumed.")
        else:
            await ctx.send("❌ Nothing is paused.")

    @commands.command(name='pause', help='Pause the current song')
    async def pause(self, ctx):
        """Pause the current song"""
        if not ctx.voice_client:
            await ctx.send("❌ Not connected to a voice channel.")
            return
        
        if ctx.voice_client.is_playing():
            ctx.voice_client.pause()
            await ctx.send("⏸️ Paused.")
        else:
            await ctx.send("❌ Nothing is playing.")

    @commands.command(name='skip', help='Skip the current song')
    async def skip(self, ctx):
        """Skip the current song"""
        if not ctx.voice_client or not ctx.voice_client.is_playing():
            await ctx.send("❌ Nothing is playing.")
            return
        
        ctx.voice_client.stop()
        await ctx.send("⏭️ Skipped.")

    @commands.command(name='stop', help='Stop playing and clear queue')
    async def stop(self, ctx):
        """Stop playing and clear the queue"""
        if not ctx.voice_client:
            await ctx.send("❌ Not connected to a voice channel.")
            return
        
        self.queue.clear()
        self.is_playing = False
        self.current = None
        ctx.voice_client.stop()
        
        await ctx.send("⏹️ Stopped and cleared queue.")
        await ctx.voice_client.disconnect()

    @commands.command(name='queue', help='Show the current queue')
    async def queue(self, ctx):
        """Show the current queue"""
        if not self.queue and not self.current:
            await ctx.send("❌ Queue is empty.")
            return
        
        embed = discord.Embed(title="🎵 Queue", color=discord.Color.blurple())
        
        if self.current:
            embed.add_field(
                name="Now Playing",
                value=self.current['title'],
                inline=False
            )
        
        if self.queue:
            queue_text = "\n".join([f"{i+1}. {song['title']}" for i, song in enumerate(self.queue[:10])])
            embed.add_field(
                name="Up Next",
                value=queue_text,
                inline=False
            )
        
        await ctx.send(embed=embed)

    @commands.command(name='join', help='Join your voice channel')
    async def join(self, ctx):
        """Join the user's voice channel"""
        if not ctx.author.voice:
            await ctx.send("❌ You must be in a voice channel.")
            return
        
        channel = ctx.author.voice.channel
        if ctx.voice_client is None:
            await channel.connect()
            await ctx.send(f"✅ Joined {channel.name}")
        else:
            await ctx.voice_client.move_to(channel)
            await ctx.send(f"✅ Moved to {channel.name}")

async def setup(bot):
    await bot.add_cog(Music(bot))
