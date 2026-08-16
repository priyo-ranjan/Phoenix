import discord
from discord.ext import commands
from discord.ui import View, Button


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
            "📦 Stock: **12**"
        )
    },

    {
        "title": "🥚 EGGS",
        "description": "Collect creatures from different realms.",
        "fields": [

    (
        "① 🥚 Common Egg",
        "Contains common creatures perfect for beginners.\n"
        "💰 Price: 500 Coins\n"
        "📦 Stock: ∞\n\n"
    ),

    (
        "② 🦴 Extinct Egg",
        "Contains creatures from the Extinct Realm.\n"
        "May hatch Dire Wolves, Dodos, Smilodons and more.\n"
        "💰 Price: 2,500 Coins\n"
        "📦 Stock: 87\n\n"
    ),

    (
        "③ 🐉 Dragon Egg",
        "Contains powerful Dragon Realm creatures.\n"
        "May hatch Wyverns, Drakes and Hydras.\n"
        "💰 Price: 5,000 Coins\n"
        "📦 Stock: 41\n\n"
    ),

    (
        "④ 🔥 Mythic Egg",
        "Contains legendary beings from mythology.\n"
        "May hatch Phoenixes, Griffins and Cerberus.\n"
        "💰 Price: 10,000 Coins\n"
        "📦 Stock: 19\n\n"
    ),

    (
        "⑤ 🌌 Cosmic Egg",
        "Contains the rarest creatures in existence.\n"
        "Extremely difficult to obtain.\n"
        "💰 Price: 50,000 Coins\n"
        "📦 Stock: 3"
    )
]
    },

    {
        "title": "🎒 UTILITIES",
        "description": "Useful tools for creature hunting.",
        "fields": [

    (
        "🎯 Hunter's Net",
        "Improves your chances of successfully catching creatures.\n\n"
        "💰 Price: 1,500 Coins"
    ),

    (
        "✨ Golden Net",
        "A premium capture tool with greatly increased success rates.\n\n"
        "💰 Price: 10,000 Coins"
    ),

    (
        "🧭 Ancient Compass",
        "Guides hunters toward rare creature spawns.\n\n"
        "💰 Price: 5,000 Coins"
    ),

    (
        "🔍 Beast Tracker",
        "Tracks nearby creatures and reveals valuable information.\n\n"
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
        "Grants a small amount of experience to a creature.\n\n"
        "💰 Price: 500 Coins"
    ),

    (
        "📖 Medium XP Scroll",
        "Grants a moderate amount of experience.\n\n"
        "💰 Price: 2,000 Coins"
    ),

    (
        "📚 Large XP Scroll",
        "Provides a huge experience boost.\n\n"
        "💰 Price: 10,000 Coins"
    ),

    (
        "💎 Revive Crystal",
        "Revives a defeated creature back to battle-ready condition.\n\n"
        "💰 Price: 5,000 Coins"
    )
]
    },

    {
        "title": "🎟 TICKETS",
        "description": "Special event and progression tickets.",
        "fields": [

    (
        "🎟 Rare Spawn Ticket",
        "Increases rare creature spawn rates for a limited time.\n\n"
        "💰 Price: 5,000 Coins"
    ),

    (
        "⚡ Double XP Ticket",
        "Earn double experience from battles and activities.\n\n"
        "💰 Price: 7,500 Coins"
    ),

    (
        "👹 Boss Raid Ticket",
        "Allows participation in special boss encounters.\n\n"
        "💰 Price: 15,000 Coins"
    ),

    (
        "📉 Marketplace Tax Pass",
        "Reduces future marketplace transaction taxes.\n\n"
        "💰 Price: 25,000 Coins"
    )
]
    },

    {
        "title": "💎 GEM STORE",
        "description": "Premium rewards purchased using Gems.",
        "fields": [

    (
        "🔥 Phoenix Aura",
        "Surround your profile with a fiery Phoenix aura.\n\n"
        "💎 Price: 25 Gems"
    ),

    (
        "🐉 Dragon Aura",
        "A majestic aura inspired by ancient dragons.\n\n"
        "💎 Price: 50 Gems"
    ),

    (
        "🌌 Cosmic Aura",
        "A rare aura infused with cosmic energy.\n\n"
        "💎 Price: 100 Gems"
    ),

    (
        "✨ Animated Border",
        "A premium animated profile border.\n\n"
        "💎 Price: 250 Gems"
    )
]
    },

    {
        "title": "✨ COSMETICS",
        "description": "Customize your profile.",
        "fields": [

    (
        "🥉 Bronze Theme",
        "A simple but elegant profile appearance.\n\n"
        "💰 Price: 5,000 Coins"
    ),

    (
        "🏛 Ancient Temple Theme",
        "Decorate your profile with ancient ruins.\n\n"
        "💰 Price: 20,000 Coins"
    ),

    (
        "🐉 Dragon Kingdom Theme",
        "A powerful dragon-themed profile design.\n\n"
        "💰 Price: 50,000 Coins"
    ),

    (
        "🌋 Volcano Theme",
        "Inspired by molten lava and fiery mountains.\n\n"
        "💰 Price: 75,000 Coins"
    ),

    (
        "🌌 Cosmic Theme",
        "A legendary profile theme from beyond the stars.\n\n"
        "💰 Price: 150,000 Coins"
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


async def setup(bot):
    await bot.add_cog(Market(bot))