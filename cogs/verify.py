import discord
from discord.ext import commands

VERIFY_CHANNEL_ID = 1501286153385676831
VERIFY_ROLE_NAME = "Verified"


class Verify(commands.Cog):
    def init(self, bot):
        self.bot = bot

    @commands.command(name="verify")
    async def verify(self, ctx):

        # wrong channel
        if ctx.channel.id != VERIFY_CHANNEL_ID:

            embed = discord.Embed(
                title="❌ Wrong Channel",
                description=(
                    "You can only use ~verify "
                    "inside the verification channel."
                ),
                color=0xff0000
            )

            msg = await ctx.send(embed=embed)

            await ctx.message.delete()

            await msg.delete(delay=5)

            return

        role = discord.utils.get(ctx.guild.roles, name=VERIFY_ROLE_NAME)

        # role not found
        if role is None:

            embed = discord.Embed(
                title="⚠ Verification Failed",
                description="Verified role was not found.",
                color=0xff0000
            )

            await ctx.send(embed=embed)

            return

        # already verified
        if role in ctx.author.roles:

            embed = discord.Embed(
                title="✨ Already Verified",
                description="You are already verified.",
                color=0x00ffff
            )

            msg = await ctx.send(embed=embed)

            await ctx.message.delete()

            await msg.delete(delay=5)

            return

        # give role
        await ctx.author.add_roles(role)

        embed = discord.Embed(
            title="🌌 Verification Successful",
            description=(
                "```yaml\n"
                "Access Granted.\n"
                "Welcome to The Nexus.\n"
                "```"
            ),
            color=0x7b2cbf
        )

        embed.set_thumbnail(url=ctx.author.display_avatar.url)

        embed.set_footer(
            text=f"Verified as {ctx.author}",
            icon_url=ctx.author.display_avatar.url
        )

        msg = await ctx.send(embed=embed)

        # delete verify command
        await ctx.message.delete()

        # auto delete embed after 5 sec
        await msg.delete(delay=5)


async def setup(bot):
    await bot.add_cog(Verify(bot))