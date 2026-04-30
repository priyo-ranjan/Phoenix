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



    @commands.command(name="mute", help="Mute a member in the server.")
    @commands.has_permissions(manage_roles=True)
    async def mute(self, ctx, member: discord.Member, minutes: int, *, reason=None):
       reason = reason or "No reason provided"
       muted_role = discord.utils.get(ctx.guild.roles, name="Muted")
       if muted_role is None:
        await ctx.send("Muted role not found. Please create a role named 'Muted' and set the appropriate permissions.")
        return

       try:
        await member.add_roles(
            muted_role,
            reason=reason
        )
        await ctx.send(f"{member} has been muted for {minutes} minutes. Reason : {reason}")
        await asyncio.sleep(minutes * 60)
        await member.remove_roles(muted_role)
        await ctx.send(f"{member.mention} has been automatically unmuted")

       except discord.Forbidden:
        await ctx.send(f"I cannot mute {member.mention}. Their role may be higher than mine.")   




    @commands.command(name="unmute", help="Unmute a member in the server.")
    @commands.has_permissions(moderate_members=True)
    async def unmute(self, ctx, member: discord.Member):
        await member.timeout(None)
        await ctx.send(f"{member} has been unmuted.")



    @commands.command(name="Purge", help="Deletes specific number of messages from the channel.")
    @commands.has_permissions(manage_messages=True)
    async def purge(self, ctx, amount: int):
        await ctx.channel.purge(limit=amount + 1)
        msg = await ctx.send(f"Deleted {amount} messages.")
        await msg.delete(delay = 0)



async def setup(bot):   
    await bot.add_cog(Moderation(bot))