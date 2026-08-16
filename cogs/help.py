import discord
from discord.ext import commands

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def help(self, ctx):

      embed = discord.Embed(
        title="📖 Command List",
        description="Available bot commands",
        color=0x5865F2
    )

      embed.add_field(
        name="🧠 AI",
        value="!ai <prompt>",
        inline=False
    )
      embed.add_field(
        name="🥳 Fun",
        value="!roast\n!say\n!ping\n!hello",
        inline=False
    )


      embed.add_field(
        name="📈 Leveling",
        value="!rank\n!rank @user",
        inline=False
    )

      embed.add_field(
              name="🎰 Gambling",
              value="!flip (amount)\n!jackpot",
              inline=False
          )
 
      embed.add_field(
        name="💎 Reputation",
        value="!rep @user\n!reps @user",
        inline=False
    )

      embed.add_field(
        name="🧠 Memory",
        value="!remember <key> <memory>\n!memories @user\n!forget <key>",
        inline=False
    )

      embed.add_field(
        name="🛡 Moderation",
        value="!kick\n!mute\n!unmute\n!ban\n!purge <number>",
        inline=False
    )

      embed.set_footer(
        text="Phoenix Bot • Built by Priyo Ranjan"
    )

      await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Help(bot))    