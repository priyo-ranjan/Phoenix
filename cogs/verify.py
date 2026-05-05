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
                    "You can only use !verify "
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
        async with ctx.typing():
         try:
            dm_embed = discord.Embed(
              title="🌌 Welcome to The Nexus",
              description=(
                "```yaml\n"
                "Identity Confirmed.\n"
                "Verification Complete.\n"
                "Acess to The Nexus Granted.\n"
            "```\n"

                "✨ Thanks for joining our futuristic community.\n"
                "Use !help to explore Phoenix commands."
        ),
        color=0x7b2cbf
    )

            dm_embed.add_field(
               name="🤖 Features",
               value=(
                "• AI Chat\n"
                "• Levels System\n"
                "• Memory System\n"
                "• Moderation\n"
                "• Fun Commands"
        ),
               inline=False
    )

            dm_embed.add_field(
              name="🚀 Getting Started",
              value=(
                "!help → View commands\n"
                "!rank → Check level\n"
                "!server → Server info"
        ),
              inline=False
    )

            dm_embed.set_thumbnail(
                url=ctx.guild.icon.url
    )

            dm_embed.set_image(
                url="https://cdn.discordapp.com/attachments/1499252105947386088/1501296262870339624/aS5qcGc.png?ex=69fb8e99&is=69fa3d19&hm=0e71f729e7cba410fdba908d4002a36e3c3436c36af3e5a4bbe7f3d6388db447&"
    )

            dm_embed.set_footer(
                text="Powered by Phoenix",
                icon_url=ctx.guild.icon.url
    )

            await ctx.author.send(embed=dm_embed)

         except discord.Forbidden:
             pass
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