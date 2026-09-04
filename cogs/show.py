import discord
from discord.ext import commands

import database


RARITY_EMOJIS = {
    "Common": "⚪",
    "Uncommon": "🟢",
    "Rare": "🔵",
    "Very Rare": "🟣",
    "Legendary": "🟠",
    "Mythic": "🔴",
    "???": "❓"
}


REALM_EMOJIS = {
    "Common Realm": "🥚",
    "Extinct Realm": "🦴",
    "Dragon Realm": "🐉",
    "Mythic Realm": "✨",
    "Cosmic Realm": "🌌"
}


class Show(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="show", aliases = ["s"])
    async def show(self, ctx, creature_number: int = None):

        # No number supplied
        if creature_number is None:

            embed = discord.Embed(
                title="🐾 SHOW CREATURE",
                description=(
                    "Specify the number of the creature you want to view.\n\n"
                    "**Example:**\n"
                    "`!show 5`"
                ),
                color=discord.Color.purple()
            )

            await ctx.send(embed=embed)
            return

        # Invalid number
        if creature_number < 1:

            embed = discord.Embed(
                title="❌ Invalid Creature Number",
                description="Creature numbers must be **1 or higher**.",
                color=discord.Color.red()
            )

            await ctx.send(embed=embed)
            return

        # Find the creature belonging to this user
        creature = await database.get_user_creature_instance(
            ctx.author.id,
            creature_number
        )

        if creature is None:

            embed = discord.Embed(
                title="❌ Creature Not Found",
                description=(
                    f"You don't own a creature with the number "
                    f"**#{creature_number}**."
                ),
                color=discord.Color.red()
            )

            await ctx.send(embed=embed)
            return

        # Database result
        number = creature[0]
        creature_id = creature[1]
        creature_name = creature[2]
        rarity = creature[3]
        realm = creature[4]

        rarity_emoji = RARITY_EMOJIS.get(
            rarity,
            "❔"
        )

        realm_emoji = REALM_EMOJIS.get(
            realm,
            "🌍"
        )

        embed = discord.Embed(
            title=f"🐾 CREATURE #{number}",
            description=f"**{creature_name}**",
            color=discord.Color.purple()
        )

        embed.add_field(
            name="✨ Rarity",
            value=f"{rarity_emoji} **{rarity}**",
            inline=True
        )

        embed.add_field(
            name="🌌 Realm",
            value=f"{realm_emoji} **{realm}**",
            inline=True
        )

        embed.add_field(
            name="🔢 Creature ID",
            value=f"`#{number}`",
            inline=True
        )

        embed.set_footer(
            text=f"Owned by {ctx.author.display_name}"
        )

        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Show(bot))