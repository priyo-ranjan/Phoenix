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


CREATURES_PER_PAGE = 20


class CollectionView(discord.ui.View):

    def __init__(self, ctx, creatures):
        super().__init__(timeout=120)

        self.ctx = ctx
        self.creatures = creatures
        self.page = 0

        self.total_pages = (
            len(creatures) + CREATURES_PER_PAGE - 1
        ) // CREATURES_PER_PAGE

        self.update_buttons()

    def update_buttons(self):

        self.previous_button.disabled = self.page == 0

        self.next_button.disabled = (
            self.page >= self.total_pages - 1
        )

    def create_embed(self):

        start = self.page * CREATURES_PER_PAGE
        end = start + CREATURES_PER_PAGE

        page_creatures = self.creatures[start:end]

        lines = []

        for index, creature in enumerate(
            page_creatures,
            start=start + 1
        ):

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

            lines.append(
                f"**#{index}** "
                f"{realm_emoji} **{creature_name}** "
                f"{rarity_emoji} {rarity}"
            )

        description = "\n".join(lines)

        embed = discord.Embed(
            title=f"🐾 {self.ctx.author.display_name.upper()}'S CREATURES",
            description=description,
            color=discord.Color.purple()
        )

        embed.set_footer(
            text=(
                f"{len(self.creatures)} creature instance(s) "
                f"• Page {self.page + 1}/{self.total_pages}"
            )
        )

        return embed

    async def interaction_check(self, interaction):

        if interaction.user.id != self.ctx.author.id:

            await interaction.response.send_message(
                "❌ This isn't your creature collection.",
                ephemeral=True
            )

            return False

        return True

    @discord.ui.button(
        label="◀",
        style=discord.ButtonStyle.secondary
    )
    async def previous_button(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):

        if self.page > 0:
            self.page -= 1

        self.update_buttons()

        await interaction.response.edit_message(
            embed=self.create_embed(),
            view=self
        )

    @discord.ui.button(
        label="▶",
        style=discord.ButtonStyle.secondary
    )
    async def next_button(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):

        if self.page < self.total_pages - 1:
            self.page += 1

        self.update_buttons()

        await interaction.response.edit_message(
            embed=self.create_embed(),
            view=self
        )

    async def on_timeout(self):

        self.previous_button.disabled = True
        self.next_button.disabled = True


class Collection(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    # --------------------------------
    # !CREATURES
    # --------------------------------

    @commands.command(
        name="creatures",
        aliases=["c"]
    )
    async def creatures(self, ctx):

        """
        Shows the user's complete numbered creature collection.
        """

        user_id = ctx.author.id

        creatures = await database.get_user_creatures(
            user_id
        )

        if not creatures:

            embed = discord.Embed(
                title="🐾 CREATURE COLLECTION",
                description=(
                    "You don't have any creatures yet.\n\n"
                    "Hatch an egg to begin your collection!"
                ),
                color=discord.Color.purple()
            )

            await ctx.send(embed=embed)
            return

        view = CollectionView(
            ctx,
            creatures
        )

        await ctx.send(
            embed=view.create_embed(),
            view=view
        )

    # --------------------------------
    # !SC / !SEARCHCREATURE
    # --------------------------------

    @commands.command(
        name="searchcreature",
        aliases=["search", "sc"]
    )
    async def searchcreature(
        self,
        ctx,
        *search_terms
    ):

        """
        Searches the user's creature collection
        by creature name.
        """

        # --------------------------------
        # NO SEARCH TERM
        # --------------------------------

        if not search_terms:

            embed = discord.Embed(
                title="🔎 CREATURE SEARCH",
                description=(
                    "Enter the name of the creature you want to search for.\n\n"
                    "**Examples:**\n"
                    "`!sc nebula`\n"
                    "`!sc dragon`\n"
                    "`!sc celestial phoenix`"
                ),
                color=discord.Color.purple()
            )

            await ctx.send(embed=embed)
            return

        # Join multiple words together
        search_term = " ".join(search_terms).strip()

        # --------------------------------
        # SEARCH DATABASE
        # --------------------------------

        matches = await database.search_user_creatures(
            ctx.author.id,
            search_term
        )

        # --------------------------------
        # NO MATCHES
        # --------------------------------

        if not matches:

            embed = discord.Embed(
                title="🔎 CREATURE SEARCH",
                description=(
                    f"No creatures found matching "
                    f"**{search_term}**."
                ),
                color=discord.Color.purple()
            )

            await ctx.send(embed=embed)
            return

        # --------------------------------
        # CREATE RESULT LIST
        # --------------------------------

        # Get the user's full collection so that
        # we can determine the permanent collection
        # number of each matching creature.
        all_creatures = await database.get_user_creatures(
            ctx.author.id
        )

        # Map database ID -> collection number
        creature_numbers = {
            creature[0]: index
            for index, creature in enumerate(
                all_creatures,
                start=1
            )
        }

        lines = []

        for creature in matches:

            database_id = creature[0]
            creature_name = creature[2]
            rarity = creature[3]
            realm = creature[4]

            collection_number = creature_numbers.get(
                database_id
            )

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
                f"{rarity_emoji}"
            )

        # --------------------------------
        # SEARCH EMBED
        # --------------------------------

        embed = discord.Embed(
            title="🔎 CREATURE SEARCH",
            description=(
                f"Results for **{search_term}**\n\n"
                + "\n".join(lines)
            ),
            color=discord.Color.purple()
        )

        embed.set_footer(
            text=f"{len(matches)} matching creature instance(s)"
        )

        await ctx.send(
            embed=embed
        )


async def setup(bot):
    await bot.add_cog(Collection(bot))