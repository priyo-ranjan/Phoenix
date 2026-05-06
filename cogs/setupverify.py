import discord
from discord.ext import commands

class SetupVerify(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def setupverify(self, ctx):
        embed = discord.Embed(
            title="✦ PHOENIX | VERIFICATION",
            description=(
               "Welcome to The Nexus.\n"
                "Access to the server is restricted until verification.\n\n"
                "Enter the command below to unlock the community."
            ),
            color=0xbb86fc
        )

        embed.add_field(
            name="🔓 Verification Command",
            value="!verify",
            inline=False
        )
        embed.add_field(
            name="📜 Before Entering",
            value=(
                "• Read the rules carefully\n"
                "• Respect the community\n"
                "• Keep the vibe clean"
            ),
            inline=False
        )
        embed.set_image(
            url="https://cdn.discordapp.com/attachments/1499252105947386088/1501674704077848726/NjEyLmpwZw.png?ex=69fcef0d&is=69fb9d8d&hm=b9df68d619e9674a15c12903525692d78a4a012c291b42822805c74008d5d5a8&"
        )
        embed.set_footer(
            text="Phoenix Verification System • Rise Together. Shine Forever."
        )  
        await ctx.send(embed=embed)

        try:
            await ctx.message.delete()
        except:
            pass

async def setup(bot):
    await bot.add_cog(SetupVerify(bot))