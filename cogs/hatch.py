import re
import unicodedata
from collections import Counter

import discord
from discord.ext import commands

import database
from .hatching import hatch_creature


EGG_ITEMS = {
    "common": "common_egg",
    "extinct": "extinct_egg",
    "dragon": "dragon_egg",
    "mythic": "mythic_egg",
    "cosmic": "cosmic_egg",
}


REALM_NAMES = {
    "common": "Common Realm",
    "extinct": "Extinct Realm",
    "dragon": "Dragon Realm",
    "mythic": "Mythic Realm",
    "cosmic": "Cosmic Realm",
}


RARITY_EMOJIS = {
    "Common": "⚪",
    "Uncommon": "🟢",
    "Rare": "🔵",
    "Very Rare": "🟣",
    "Legendary": "🟠",
    "Mythic": "🔴",
    "???": "❓",
}


def creature_item_id(egg_type, creature_name):
    """
    Converts a creature name into a safe inventory item ID.

    The realm is included so duplicate creature names
    from different realms don't collide.
    """

    normalized = unicodedata.normalize("NFKD", creature_name)
    normalized = normalized.encode("ascii", "ignore").decode("ascii")

    normalized = normalized.lower()
    normalized = re.sub(r"[^a-z0-9]+", "_", normalized)
    normalized = normalized.strip("_")

    return f"{egg_type}_{normalized}"


class Hatch(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="hatch", aliases=["h"])
    async def hatch(self, ctx, egg_type: str = None, amount: int = 1):
        """
        Hatch one or multiple eggs.

        Usage:
        !hatch common
        !hatch common 5
        !hatch cosmic 10
        """
        egg_aliases = {
        "ce": "common",
        "ee": "extinct",
        "de": "dragon",
        "me": "mythic",
        "cse": "cosmic",
    }

        if egg_type is not None:
         egg_type = egg_aliases.get(egg_type.lower(), egg_type.lower())

        # No egg type supplied
        if egg_type is None:
            embed = discord.Embed(
                title="🥚 Hatch an Egg",
                description=(
                    "Specify an egg type and optionally an amount.\n\n"
                    "**Available eggs:**\n"
                    "🥚 `common`\n"
                    "🦴 `extinct`\n"
                    "🐉 `dragon`\n"
                    "✨ `mythic`\n"
                    "🌌 `cosmic`\n\n"
                    "**Examples:**\n"
                    "`!hatch common`\n"
                    "`!hatch cosmic 10`"
                ),
                color=discord.Color.purple()
            )

            await ctx.send(embed=embed)
            return

        egg_type = egg_type.lower()

        # Invalid egg type
        if egg_type not in EGG_ITEMS:
            embed = discord.Embed(
                title="❌ Invalid Egg",
                description=(
                    f"`{egg_type}` is not a valid egg type.\n\n"
                    "**Available eggs:**\n"
                    "🥚 `common`\n"
                    "🦴 `extinct`\n"
                    "🐉 `dragon`\n"
                    "✨ `mythic`\n"
                    "🌌 `cosmic`"
                ),
                color=discord.Color.red()
            )

            await ctx.send(embed=embed)
            return

        # Invalid amount
        if amount < 1:
            embed = discord.Embed(
                title="❌ Invalid Amount",
                description="The amount must be at least **1**.",
                color=discord.Color.red()
            )

            await ctx.send(embed=embed)
            return

        user_id = ctx.author.id
        egg_item = EGG_ITEMS[egg_type]

        # Check whether the user owns enough eggs
        has_eggs = await database.has_item(
            user_id,
            egg_item,
            amount
        )

        if not has_eggs:
            owned = await database.get_item_count(
                user_id,
                egg_item
            )

            embed = discord.Embed(
                title="🥚 Not Enough Eggs",
                description=(
                    f"You tried to hatch **{amount:,}** "
                    f"{REALM_NAMES[egg_type]} eggs.\n\n"
                    f"You only have **{owned:,}**."
                ),
                color=discord.Color.red()
            )

            await ctx.send(embed=embed)
            return

        # Roll every creature BEFORE changing the database.
        # This prevents losing eggs if the hatch engine fails.
        creatures = []

        for _ in range(amount):
            creature = hatch_creature(egg_type)

            if creature is None:
                embed = discord.Embed(
                    title="❌ Hatch Failed",
                    description=(
                        "Something went wrong while rolling the creatures.\n"
                        "No eggs were consumed."
                    ),
                    color=discord.Color.red()
                )

                await ctx.send(embed=embed)
                return

            creatures.append(creature)

        # Remove all eggs at once
        await database.remove_item(
            user_id,
            egg_item,
            amount
        )

        # Count duplicate creatures
        creature_counts = Counter(
            creature["name"]
            for creature in creatures
        )

        for creature_name, count in creature_counts.items():

            item_id = creature_item_id(
                egg_type,
                creature_name
            )

            await database.add_item(
                user_id,
                item_id,
                count
            )
        # Create a permanent instance for every creature hatched
        for creature in creatures:

            item_id = creature_item_id(
                egg_type,
                creature["name"]
            )

            creature_number = await database.add_creature_instance(
                user_id=user_id,
                creature_id=item_id,
                creature_name=creature["name"],
                rarity=creature["rarity"],
                realm=REALM_NAMES[egg_type]
            )

        # SINGLE HATCH
        if amount == 1:

            creature = creatures[0]
            creature_name = creature["name"]
            rarity = creature["rarity"]

            rarity_emoji = RARITY_EMOJIS.get(
                rarity,
                "❔"
            )

            embed = discord.Embed(
                title="🥚✨ EGG HATCHED!",
                description=(
                    f"**{ctx.author.display_name}** hatched an egg "
                    f"from the **{REALM_NAMES[egg_type]}**!"
                ),
                color=discord.Color.purple()
            )

            embed.add_field(
                name="🐾 Creature",
                value=f"**{creature_name}**",
                inline=False
            )

            embed.add_field(
                name="✨ Rarity",
                value=f"{rarity_emoji} **{rarity}**",
                inline=True
            )

            embed.add_field(
                name="🌌 Realm",
                value=f"**{REALM_NAMES[egg_type]}**",
                inline=True
            )

            embed.set_footer(
                text="The creature has been added to your collection."
            )

            await ctx.send(embed=embed)
            return

        # MULTIPLE HATCHES

        # Group results by rarity
        rarity_counts = Counter(
            creature["rarity"]
            for creature in creatures
        )

        result_lines = []

        for creature_name, count in creature_counts.items():

            # Find rarity for this creature
            rarity = next(
                creature["rarity"]
                for creature in creatures
                if creature["name"] == creature_name
            )

            emoji = RARITY_EMOJIS.get(
                rarity,
                "❔"
            )

            result_lines.append(
                f"{emoji} **{creature_name}** ×{count:,}"
                f" — {rarity}"
            )

        rarity_lines = []

        for rarity, count in rarity_counts.items():

            emoji = RARITY_EMOJIS.get(
                rarity,
                "❔"
            )

            rarity_lines.append(
                f"{emoji} **{rarity}:** {count:,}"
            )

        embed = discord.Embed(
            title=f"🥚✨ {amount:,} EGGS HATCHED!",
            description=(
                f"**{ctx.author.display_name}** hatched "
                f"**{amount:,} eggs** from the "
                f"**{REALM_NAMES[egg_type]}**!\n\n"
                f"### 🐾 Creatures Obtained\n"
                + "\n".join(result_lines)
                + "\n\n### ✨ Rarity Results\n"
                + "\n".join(rarity_lines)
            ),
            color=discord.Color.purple()
        )

        embed.set_footer(
            text="All creatures have been added to your collection."
        )

        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Hatch(bot))