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


class Favorites(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    # --------------------------------
    # !FAV
    # --------------------------------

    @commands.command(name="fav")
    async def fav(self, ctx, *creature_numbers: int):

        # --------------------------------
        # NO NUMBERS
        # SHOW FAVORITES
        # --------------------------------

        if not creature_numbers:

            creatures = await database.get_favorite_creatures(
                ctx.author.id
            )

            if not creatures:

                embed = discord.Embed(
                    title="⭐ FAVORITE CREATURES",
                    description=(
                        "You don't have any favorite creatures yet.\n\n"
                        "**Example:**\n"
                        "`!fav 1 18 20`"
                    ),
                    color=discord.Color.gold()
                )

                await ctx.send(embed=embed)
                return

            # Get the complete collection so we can determine
            # the current collection number of each favorite.
            all_creatures = await database.get_user_creatures(
                ctx.author.id
            )

            # Map database ID -> current collection number
            number_map = {
                creature[0]: index
                for index, creature in enumerate(
                    all_creatures,
                    start=1
                )
            }

            lines = []

            for creature in creatures:

                database_id = creature[0]
                creature_name = creature[2]
                rarity = creature[3]
                realm = creature[4]

                collection_number = number_map.get(
                    database_id
                )

                if collection_number is None:
                    continue

                rarity_emoji = RARITY_EMOJIS.get(
                    rarity,
                    "❔"
                )

                realm_emoji = REALM_EMOJIS.get(
                    realm,
                    "🌍"
                )

                lines.append(
                    f"**#{collection_number}** "
                    f"{realm_emoji} **{creature_name}** "
                    f"{rarity_emoji} {rarity}"
                )

            embed = discord.Embed(
                title=(
                    f"⭐ {ctx.author.display_name.upper()}"
                    f"'S FAVORITES"
                ),
                description="\n".join(lines),
                color=discord.Color.gold()
            )

            embed.set_footer(
                text=f"{len(lines)} favorite creature(s)"
            )

            await ctx.send(embed=embed)
            return

        # --------------------------------
        # FAVORITE SPECIFIC CREATURES
        # --------------------------------

        successful = []
        already_favorite = []
        invalid = []

        for number in creature_numbers:

            if number < 1:
                invalid.append(number)
                continue

            creature = await database.get_user_creature_instance(
                ctx.author.id,
                number
            )

            if creature is None:
                invalid.append(number)
                continue

            database_id = creature[0]

            favorites = await database.get_favorite_creatures(
                ctx.author.id
            )

            favorite_ids = {
                favorite[0]
                for favorite in favorites
            }

            if database_id in favorite_ids:
                already_favorite.append(number)
                continue

            await database.add_favorite_creature(
                ctx.author.id,
                database_id
            )

            successful.append(number)

        # --------------------------------
        # RESPONSE
        # --------------------------------

        description = ""

        if successful:
            description += (
                "⭐ **Favorited:** "
                + ", ".join(f"#{n}" for n in successful)
                + "\n"
            )

        if already_favorite:
            description += (
                "⚠️ **Already favorited:** "
                + ", ".join(f"#{n}" for n in already_favorite)
                + "\n"
            )

        if invalid:
            description += (
                "❌ **Not found:** "
                + ", ".join(f"#{n}" for n in invalid)
            )

        embed = discord.Embed(
            title="⭐ FAVORITES UPDATED",
            description=description,
            color=discord.Color.gold()
        )

        await ctx.send(embed=embed)

    # --------------------------------
    # !UNFAV
    # --------------------------------

    @commands.command(name="unfav")
    async def unfav(self, ctx, *creature_numbers: int):

        if not creature_numbers:

            embed = discord.Embed(
                title="⭐ REMOVE FAVORITE",
                description=(
                    "Specify the number(s) of the creatures "
                    "you want to unfavorite.\n\n"
                    "**Example:**\n"
                    "`!unfav 1 18 20`"
                ),
                color=discord.Color.red()
            )

            await ctx.send(embed=embed)
            return

        removed = []
        not_favorite = []
        invalid = []

        for number in creature_numbers:

            if number < 1:
                invalid.append(number)
                continue

            creature = await database.get_user_creature_instance(
                ctx.author.id,
                number
            )

            if creature is None:
                invalid.append(number)
                continue

            database_id = creature[0]

            was_removed = await database.remove_favorite_creature(
                ctx.author.id,
                database_id
            )

            if was_removed:
                removed.append(number)
            else:
                not_favorite.append(number)

        # --------------------------------
        # RESPONSE
        # --------------------------------

        description = ""

        if removed:
            description += (
                "💔 **Unfavorited:** "
                + ", ".join(f"#{n}" for n in removed)
                + "\n"
            )

        if not_favorite:
            description += (
                "⚠️ **Not favorited:** "
                + ", ".join(f"#{n}" for n in not_favorite)
                + "\n"
            )

        if invalid:
            description += (
                "❌ **Not found:** "
                + ", ".join(f"#{n}" for n in invalid)
            )

        embed = discord.Embed(
            title="⭐ FAVORITES UPDATED",
            description=description,
            color=discord.Color.gold()
        )

        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Favorites(bot))