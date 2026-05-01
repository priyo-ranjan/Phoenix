import discord
from discord.ext import commands
import json
class Rep(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.cooldown(1, 86400, commands.BucketType.user)
    @commands.command()
    async def rep(self, ctx, member: discord.Member):

        if member == ctx.author:
            await ctx.send("You cannot give reputation to yourself 💀")
            return
        with open("rep.json", "r") as f:
            users = json.load(f)
        user_id = str(member.id)

        if user_id not in users:
            users[user_id] = {
                "rep":0
            }

        users[user_id]["rep"] += 1

        with open("rep.json", "w") as f:
            json.dump(users, f, indent = 4)

        embed = discord.Embed(
            title = "Reputation Given!",
            description = (f"{ctx.author.mention} has given a reputation point to" f"{member.mention}!"),
            color = 0x5865F2
        )
        embed.set_thumbnail(url = member.avatar.url)
        embed.add_field(
            name = "Total Reputation",
            value = users[user_id]["rep"]
        )
        await ctx.send(embed = embed)
    @rep.error
    async def rep_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            hours = round(error.retry_after / 3600, 1)
            embed = discord.Embed(
                description = (
                    f"You can give reputation again in " f"{hours} hours!"
                ),
                color = 0xff0000
            )
            await ctx.send(embed = embed)

async def setup(bot):
    await bot.add_cog(Rep(bot))