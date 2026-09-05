import discord
from discord.ext import commands
from .creatures import CREATURES
import database
import os


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

    @commands.command(name="show", aliases=["s"])
    async def show(self, ctx, creature_number: int = None):

        # --------------------------------
        # NO NUMBER SUPPLIED
        # --------------------------------

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

        # --------------------------------
        # INVALID NUMBER
        # --------------------------------

        if creature_number < 1:

            embed = discord.Embed(
                title="❌ Invalid Creature Number",
                description="Creature numbers must be **1 or higher**.",
                color=discord.Color.red()
            )

            await ctx.send(embed=embed)
            return

        # --------------------------------
        # FIND USER'S CREATURE
        # --------------------------------

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

        # --------------------------------
        # DATABASE DATA
        # --------------------------------

        number = creature[0]
        creature_name = creature[2]
        rarity = creature[3]
        realm = creature[4]

        # --------------------------------
        # FIND CREATURE IMAGE
        # --------------------------------

        image_path = None

        for creature_list in CREATURES.values():

            for data in creature_list:

                if data["name"].lower() == creature_name.lower():

                    image_path = data.get("image")
                    break

            if image_path:
                break

        # --------------------------------
        # EMOJIS
        # --------------------------------

        rarity_emoji = RARITY_EMOJIS.get(
            rarity,
            "❔"
        )

        realm_emoji = REALM_EMOJIS.get(
            realm,
            "🌍"
        )

        # --------------------------------
        # CREATE EMBED
        # --------------------------------

        embed = discord.Embed(
            title=f"🐾 CREATURE",
            description=f"**{creature_name}**",
            color=discord.Color.purple()
        )

        # Rarity displayed directly
        embed.add_field(
            name=f"{rarity_emoji} {rarity}",
            value="\u200b",
            inline=True
        )

        # Realm displayed directly
        embed.add_field(
            name=f"{realm_emoji} {realm}",
            value="\u200b",
            inline=True
        )

        embed.set_footer(
            text=f"Owned by {ctx.author.display_name}"
        )

        # --------------------------------
        # SEND CREATURE IMAGE
        # --------------------------------

        if image_path:

            # Project root directory
            base_dir = os.path.dirname(
                os.path.dirname(
                    os.path.abspath(__file__)
                )
            )

            # Full path to image
            full_image_path = os.path.join(
                base_dir,
                image_path
            )

            # Check that image actually exists
            if os.path.exists(full_image_path):

                image_filename = os.path.basename(
                    full_image_path
                )

                file = discord.File(
                    full_image_path,
                    filename=image_filename
                )

                embed.set_image(
                    url=f"attachment://{image_filename}"
                )

                await ctx.send(
                    embed=embed,
                    file=file
                )

                return

        # --------------------------------
        # SEND NORMAL EMBED
        # IF IMAGE DOESN'T EXIST
        # --------------------------------

        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Show(bot))