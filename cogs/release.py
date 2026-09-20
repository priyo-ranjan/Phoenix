import discord
from discord.ext import commands

import database


class Release(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="release", aliases=["r"])
    async def release(self, ctx, *creature_numbers: int):

        # No numbers provided
        if not creature_numbers:

            embed = discord.Embed(
                title="🗑️ RELEASE CREATURE",
                description=(
                    "Specify the number(s) of the creature(s) "
                    "you want to release.\n\n"
                    "**Examples:**\n"
                    "`!r 8`\n"
                    "`!r 8 7 10`\n"
                    "`!r 1 5 12 20`"
                ),
                color=discord.Color.orange()
            )

            await ctx.send(embed=embed)
            return

        user_id = ctx.author.id

        # Remove duplicate numbers
        creature_numbers = list(dict.fromkeys(creature_numbers))

        # Get the user's CURRENT collection
        creatures = await database.get_user_creatures(user_id)

        if not creatures:

            embed = discord.Embed(
                title="❌ EMPTY COLLECTION",
                description="You don't have any creatures to release.",
                color=discord.Color.red()
            )

            await ctx.send(embed=embed)
            return

        # Current collection position -> creature
        creature_lookup = {
            index + 1: creature
            for index, creature in enumerate(creatures)
        }

        # Check all requested numbers BEFORE deleting anything
        invalid_numbers = [
            number
            for number in creature_numbers
            if number < 1 or number not in creature_lookup
        ]

        if invalid_numbers:

            invalid_text = ", ".join(
                f"`#{number}`"
                for number in invalid_numbers
            )

            embed = discord.Embed(
                title="❌ INVALID CREATURE NUMBER",
                description=(
                    f"The following creature number(s) don't exist:\n\n"
                    f"{invalid_text}\n\n"
                    f"Your collection currently contains "
                    f"**{len(creatures)}** creature(s)."
                ),
                color=discord.Color.red()
            )

            await ctx.send(embed=embed)
            return

        # Save the ORIGINAL creatures before deletion
        selected_creatures = [
            creature_lookup[number]
            for number in creature_numbers
        ]

        # Keep track of ONLY creatures that were actually released
        released_creatures = []

        # IMPORTANT:
        # Delete from highest number to lowest number.
        # This prevents collection-number shifting.
        for number in sorted(creature_numbers, reverse=True):

            # Get the original creature from the collection
            creature = creature_lookup[number]

            # Database ID of this exact creature instance
            database_id = creature[0]

            # Check if this creature is favorited
            if await database.is_favorite_creature(
                user_id,
                database_id
            ):

                await ctx.send(
                    f"⭐ **#{number} is one of your favorite creatures!**\n"
                    f"Unfavorite it first using `!unfav {number}` "
                    f"before releasing it."
                )

                # Do NOT release it
                continue

            # Release the creature
            result = await database.release_creature_instance(
                user_id,
                number
            )

            # Only add it to the released list if it was actually released
            if result is not None:
                released_creatures.append(
                    (number, creature)
                )

        # If nothing was released
        if not released_creatures:

            embed = discord.Embed(
                title="🗑️ CREATURES RELEASED",
                description=(
                    "No creatures were released.\n\n"
                    "All selected creatures are either favorites "
                    "or could not be released."
                ),
                color=discord.Color.orange()
            )

            embed.set_footer(
                text="0 creature(s) released"
            )

            await ctx.send(embed=embed)
            return

        # Build result message
        lines = []

        # Sort back into the order the user originally entered
        released_creatures.sort(
            key=lambda item: creature_numbers.index(item[0])
        )

        for number, creature in released_creatures:

            creature_name = creature[2]
            rarity = creature[3]

            lines.append(
                f"**#{number}** — {creature_name} "
                f"({rarity})"
            )

        embed = discord.Embed(
            title="🗑️ CREATURES RELEASED",
            description="\n".join(lines),
            color=discord.Color.orange()
        )

        embed.set_footer(
            text=f"{len(released_creatures)} creature(s) released"
        )

        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Release(bot))