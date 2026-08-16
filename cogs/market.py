import discord
from discord.ext import commands
from discord.ui import View, Button
import database

ITEM_PRICES = {
    "common_egg": 500,
    "extinct_egg": 2500,
    "dragon_egg": 5000,
    "mythic_egg": 10000,
    "cosmic_egg": 50000,

    "hunters_net": 1500,
    "golden_net": 10000,
    "ancient_compass": 5000,
    "beast_tracker": 15000,

    "small_xp_scroll": 500,
    "medium_xp_scroll": 2000,       
    "large_xp_scroll": 10000,
    "revive_crystal": 5000,

    "rare_spawn_ticket": 5000,
    "double_xp_ticket": 7500,
    "boss_raid_ticket": 15000,
    "marketplace_tax_pass": 25000,

    "phoenix_aura": 25,
    "dragon_aura": 50,
    "cosmic_aura": 100,
    "animated_border": 250,

    "bronze_theme": 5000,
    "ancient_temple_theme": 20000,
    "dragon_kingdom_theme": 50000,
    "volcano_theme": 75000,
    "cosmic_theme": 150000
}

GEM_ITEMS = {
    "phoenix_aura",
    "dragon_aura",
    "cosmic_aura",
    "animated_border"
}

MARKET_PAGES = [
    {
        "title": "🏪 PHOENIX MARKET",
        "description": (
            "```yaml\n"
            "Welcome to the Official Phoenix Marketplace\n"
            "Purchase items, eggs, boosters and cosmetics.\n"
            "```"
        ),
        "fields": [
            (
                "🥚 __EGGS__",
                "```fix\nHatch and collect powerful creatures\n```"
            ),
            (
                "🎒 __UTILITIES__",
                "```fix\nTools to help your journey\n```"
            ),
            (
                "📦 __CONSUMABLES__",
                "```fix\nOne-time use items\n```"
            ),
            (
                "🎟 __TICKETS__",
                "```fix\nSpecial bonuses and events\n```"
            ),
            (
                "💎 __GEM STORE__",
                "```fix\nPremium cosmetics and effects\n```"
            ),
            (
                "✨ __COSMETICS__",
                "```fix\nThemes, borders and visual upgrades\n```"
            )
        ],
        "featured": (
            "🐉 **Dragon Egg**\n"
            "~~5,000 Coins~~ → **4,000 Coins**\n"
        )
    },

    {
        "title": "🥚 EGGS",
        "description": "Collect creatures from different realms.",
        "fields": [

    (
        "① 🥚 Common Egg",
        "Contains common creatures perfect for beginners.\n"
        "💰 Price: 500 Coins\n\n"
    ),

    (
        "② 🦴 Extinct Egg",
        "Contains creatures from the Extinct Realm.\n"
        "May hatch Dire Wolves, Dodos, Smilodons and more.\n"
        "💰 Price: 2,500 Coins\n\n"
    ),

    (
        "③ 🐉 Dragon Egg",
        "Contains powerful Dragon Realm creatures.\n"
        "May hatch Wyverns, Drakes and Hydras.\n"
        "💰 Price: 5,000 Coins\n\n"
    ),

    (
        "④ 🔥 Mythic Egg",
        "Contains legendary beings from mythology.\n"
        "May hatch Phoenixes, Griffins and Cerberus.\n"
        "💰 Price: 10,000 Coins\n\n"
    ),

    (
        "⑤ 🌌 Cosmic Egg",
        "Contains the rarest creatures in existence.\n"
        "Extremely difficult to obtain.\n"
        "💰 Price: 50,000 Coins\n"
    )
]
    },

    {
        "title": "🎒 UTILITIES",
        "description": "Useful tools for creature hunting.",
        "fields": [

    (
        "🎯 Hunter's Net",
        "Improves your chances of successfully catching creatures.\n"
        "💰 Price: 1,500 Coins\n\n"
    ),

    (
        "✨ Golden Net",
        "A premium capture tool with greatly increased success rates.\n"
        "💰 Price: 10,000 Coins\n\n"
    ),

    (
        "🧭 Ancient Compass",
        "Guides hunters toward rare creature spawns.\n"
        "💰 Price: 5,000 Coins\n\n"
    ),

    (
        "🔍 Beast Tracker",
        "Tracks nearby creatures and reveals valuable information.\n"
        "💰 Price: 15,000 Coins"
    )
]
    },

    {
        "title": "📦 CONSUMABLES",
        "description": "Temporary boosts and recovery items.",
        "fields": [

    (
        "📜 Small XP Scroll",
        "Grants a small amount of experience to a creature.\n"
        "💰 Price: 500 Coins\n\n"
    ),

    (
        "📖 Medium XP Scroll",
        "Grants a moderate amount of experience.\n"
        "💰 Price: 2,000 Coins\n\n"
    ),

    (
        "📚 Large XP Scroll",
        "Provides a huge experience boost.\n"
        "💰 Price: 10,000 Coins\n\n"
    ),

    (
        "💎 Revive Crystal",
        "Revives a defeated creature back to battle-ready condition.\n"
        "💰 Price: 5,000 Coins\n\n"
    )
]
    },

    {
        "title": "🎟 TICKETS",
        "description": "Special event and progression tickets.",
        "fields": [

    (
        "🎟 Rare Spawn Ticket",
        "Increases rare creature spawn rates for a limited time.\n"
        "💰 Price: 5,000 Coins\n\n"
    ),

    (
        "⚡ Double XP Ticket",
        "Earn double experience from battles and activities.\n"
        "💰 Price: 7,500 Coins\n\n"
    ),

    (
        "👹 Boss Raid Ticket",
        "Allows participation in special boss encounters.\n"
        "💰 Price: 15,000 Coins\n\n"
    ),

    (
        "📉 Marketplace Tax Pass",
        "Reduces future marketplace transaction taxes.\n"
        "💰 Price: 25,000 Coins\n\n"
    )
]
    },

    {
        "title": "💎 GEM STORE",
        "description": "Premium rewards purchased using Gems.",
        "fields": [

    (
        "🔥 Phoenix Aura",
        "Surround your profile with a fiery Phoenix aura.\n"
        "💎 Price: 25 Gems\n\n"
    ),

    (
        "🐉 Dragon Aura",
        "A majestic aura inspired by ancient dragons.\n"
        "💎 Price: 50 Gems\n\n"
    ),

    (
        "🌌 Cosmic Aura",
        "A rare aura infused with cosmic energy.\n"
        "💎 Price: 100 Gems\n\n"
    ),

    (
        "✨ Animated Border",
        "A premium animated profile border.\n"
        "💎 Price: 250 Gems\n\n"
    )
]
    },

    {
        "title": "✨ COSMETICS",
        "description": "Customize your profile.",
        "fields": [

    (
        "🥉 Bronze Theme",
        "A simple but elegant profile appearance.\n"
        "💰 Price: 5,000 Coins\n\n"
    ),

    (
        "🏛 Ancient Temple Theme",
        "Decorate your profile with ancient ruins.\n"
        "💰 Price: 20,000 Coins\n\n"
    ),

    (
        "🐉 Dragon Kingdom Theme",
        "A powerful dragon-themed profile design.\n"
        "💰 Price: 50,000 Coins\n\n"
    ),

    (
        "🌋 Volcano Theme",
        "Inspired by molten lava and fiery mountains.\n"
        "💰 Price: 75,000 Coins\n\n"
    ),

    (
        "🌌 Cosmic Theme",
        "A legendary profile theme from beyond the stars.\n"
        "💰 Price: 150,000 Coins\n\n"
    )
]
    }
]


class MarketView(View):

    def __init__(self):
        super().__init__(timeout=180)
        self.page = 0

    def create_embed(self):

        data = MARKET_PAGES[self.page]

        embed = discord.Embed(
            title=data["title"],
            description=data["description"],
            color=0xF39C12  # Gold / Orange
        )

        if self.page == 0:

            for name, value in data["fields"]:
                embed.add_field(
                    name=name,
                    value=value,
                    inline=False
                )

            embed.add_field(
                name="🔥 FEATURED ITEM",
                value=data["featured"],
                inline=False
            )

            embed.add_field(
                name="📢 MARKET NEWS",
                value=(
                    "• Dragon Egg stock replenished\n"
                    "• Mythic Egg stock running low\n"
                    "• Featured Item refreshed"
                ),
                inline=False
            )

        else:

            for name, value in data["fields"]:
                embed.add_field(
                    name=f"**{name}**",
                    value=value,
                    inline=False
                )

        embed.set_thumbnail(
            url="https://cdn-icons-png.flaticon.com/512/3144/3144456.png"
        )

        embed.set_footer(
            text=f"Phoenix Market • Page {self.page + 1}/{len(MARKET_PAGES)}"
        )

        return embed

    @discord.ui.button(label="◀ Previous", style=discord.ButtonStyle.secondary)
    async def previous(self, interaction: discord.Interaction, button: Button):

        if self.page > 0:
            self.page -= 1

        await interaction.response.edit_message(
            embed=self.create_embed(),
            view=self
        )

    @discord.ui.button(label="🏠 Home", style=discord.ButtonStyle.success)
    async def home(self, interaction: discord.Interaction, button: Button):

        self.page = 0

        await interaction.response.edit_message(
            embed=self.create_embed(),
            view=self
        )

    @discord.ui.button(label="▶ Next", style=discord.ButtonStyle.primary)
    async def next(self, interaction: discord.Interaction, button: Button):

        if self.page < len(MARKET_PAGES) - 1:
            self.page += 1

        await interaction.response.edit_message(
            embed=self.create_embed(),
            view=self
        )


class Market(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def market(self, ctx):

        view = MarketView()

        await ctx.send(
            embed=view.create_embed(),
            view=view
        )
    @commands.command(name="buy")
    async def buy(self, ctx, item_id: str, amount: int = 1):

        item_id = item_id.lower()

        if amount <= 0:
            return await ctx.send("❌ Amount must be greater than 0.")

        if item_id not in ITEM_PRICES:
            return await ctx.send(
                f"❌ Unknown item.\nUse `{ctx.prefix}market` to view available items."
        )

        price_per_item = ITEM_PRICES[item_id]
        total_price = price_per_item * amount

    # GEM ITEMS
        if item_id in GEM_ITEMS:

            if not await database.has_enough_gems(ctx.author.id, total_price):
                embed = discord.Embed(
                    title="❌ Purchase Failed",
                    description=(
                        f"You need **{total_price:,} Gems**\n"
                        f"to buy **{amount}x {item_id.replace('_', ' ').title()}**."
                    ),
                    color=discord.Color.red()
                )
                return await ctx.send(embed=embed)

            await database.remove_gems(ctx.author.id, total_price)

            currency_name = "Gems"

    # COIN ITEMS
        else:

            if not await database.has_enough_coins(ctx.author.id, total_price):
                embed = discord.Embed(
                    title="❌ Purchase Failed",
                    description=(
                        f"You need **{total_price:,} Coins**\n"
                        f"to buy **{amount}x {item_id.replace('_', ' ').title()}**."
                ),
                    color=discord.Color.red()
            )
                return await ctx.send(embed=embed)

            await database.remove_coins(ctx.author.id, total_price)

            currency_name = "Coins"

        await database.add_item(
            ctx.author.id,
            item_id,
            amount
    )

        embed = discord.Embed(
            title="🛒 Purchase Successful",
            color=discord.Color.green()
    )

        embed.add_field(
            name="📦 Item",
            value=item_id.replace("_", " ").title(),
            inline=True
    )

        embed.add_field(
            name="🔢 Quantity",
            value=str(amount),
            inline=True
    )

        embed.add_field(
            name=f"💰 Cost ({currency_name})",
            value=f"{total_price:,}",
            inline=True
    )

        embed.set_footer(
            text=f"Purchased by {ctx.author.display_name}"
    )

        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Market(bot))