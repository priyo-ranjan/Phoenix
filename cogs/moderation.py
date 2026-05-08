import discord
from discord.ext import commands
from datetime import datetime, timedelta

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="kick", help="Kick a member from the server.")
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        reason = reason or "No reason provided"
        try:
            await member.kick(reason=reason)
            await ctx.send(f"{member} has been kicked from the server. Reason : {reason}")
        except discord.Forbidden:
                await ctx.send(f"I cannot kick {member.mention}. Their role may be higher than mine.")
        except discord.HTTPException:
                    await ctx.send("Something went wrong while trying to kick the member.")
    @kick.error
    async def kick_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You don't have permission to use this command.")
        elif isinstance(error, commands.BadArgument):
            await ctx.send("Please mention a valid member to kick.")
        else:
            await ctx.send("An error occurred while trying to kick the member.")
        

    @commands.command(name="ban", help="Ban a member from the server.")
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        reason = reason or "No reason provided"
        try:
            await member.ban(reason=reason)
            await ctx.send(f"{member} has been banned from the server. Reason : {reason}")
        except discord.Forbidden:
                await ctx.send(f"I cannot ban {member.mention}. Their role may be higher than mine.")
        except discord.HTTPException:
                    await ctx.send("Something went wrong while trying to ban the member.")
    @ban.error
    async def ban_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You don't have permission to use this command.")
        elif isinstance(error, commands.BadArgument):
            await ctx.send("Please mention a valid member to ban.")
        else:
            await ctx.send("An error occurred while trying to ban the member.")



    @commands.command()
    @commands.has_permissions(moderate_members=True)
    async def mute(self, ctx, member: discord.Member, minutes: int, *, reason="No reason provided"):
        try:
            await member.timeout(
                timedelta(minutes=minutes),
                reason=reason
            )

            embed = discord.Embed(
                title="🔇 Member Timed Out",
                description=f"{member.mention} has been muted.",
                color=0x5865F2
            )

            embed.add_field(
                name="⏰ Duration",
                value=f"{minutes} minutes",
                inline=True
            )

            embed.add_field(
                name="📝 Reason",
                value=reason,
                inline=False
            )

            embed.set_thumbnail(url=member.display_avatar.url)

            embed.set_footer(
                text=f"Muted by {ctx.author}",
                icon_url=ctx.author.display_avatar.url
            )

            await ctx.send(embed=embed)
        except discord.Forbidden:
            await ctx.send(f"I cannot mute {member.mention}. Their role may be higher than mine.")
        except discord.HTTPException:
            await ctx.send("Something went wrong while trying to mute the member.")

    @mute.error
    async def mute_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You don't have permission to use this command.")
        elif isinstance(error, commands.BadArgument):
            await ctx.send("Please mention a valid member to mute.")
        else:
            await ctx.send("An error occurred while trying to mute the member.") 

    @commands.command()
    @commands.has_permissions(moderate_members=True)

    async def unmute(self, ctx, member: discord.Member):

        await member.timeout(None)

        embed = discord.Embed(
          title="🔊 Member Unmuted",
          description=f"{member.mention} can speak again.",
          color=0x57F287
    )

        await ctx.send(embed=embed)


    @commands.command(name="Purge", help="Deletes specific number of messages from the channel.")
    @commands.has_permissions(manage_messages=True)
    async def purge(self, ctx, amount: int):
        try:
            await ctx.channel.purge(limit=amount + 1)
            msg = await ctx.send(f"Deleted {amount} messages.")
            await msg.delete(delay=0)
        except discord.Forbidden:
            await ctx.send("I don't have permission to delete messages in this channel.")
        except discord.HTTPException:
            await ctx.send("Something went wrong while trying to delete the messages.")

    @purge.error
    async def purge_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You don't have permission to use this command.")
        elif isinstance(error, commands.BadArgument):
            await ctx.send("Please specify a valid number of messages to delete.")
        else:
            await ctx.send("An error occurred while trying to delete the messages.") 



async def setup(bot):   
    await bot.add_cog(Moderation(bot))