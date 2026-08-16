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
            ("① Common Egg", "💰 **500 Coins**\n📦 Stock: ∞"),
            ("② Extinct Egg", "💰 **2,500 Coins**\n📦 Stock: 87"),
            ("③ Dragon Egg", "💰 **5,000 Coins**\n📦 Stock: 41"),
            ("④ Mythic Egg", "💰 **10,000 Coins**\n📦 Stock: 19"),
            ("⑤ Cosmic Egg", "💰 **50,000 Coins**\n📦 Stock: 3")
        ]
    },

    {
        "title": "🎒 UTILITIES",
        "description": "Useful tools for creature hunting.",
        "fields": [
            ("Hunter's Net", "💰 **1,500 Coins**"),
            ("Golden Net", "💰 **10,000 Coins**"),
            ("Ancient Compass", "💰 **5,000 Coins**"),
            ("Beast Tracker", "💰 **15,000 Coins**")
        ]
    },

    {
        "title": "📦 CONSUMABLES",
        "description": "Temporary boosts and recovery items.",
        "fields": [
            ("Small XP Scroll", "💰 **500 Coins**"),
            ("Medium XP Scroll", "💰 **2,000 Coins**"),
            ("Large XP Scroll", "💰 **10,000 Coins**"),
            ("Revive Crystal", "💰 **5,000 Coins**")
        ]
    },

    {
        "title": "🎟 TICKETS",
        "description": "Special event and progression tickets.",
        "fields": [
            ("Rare Spawn Ticket", "💰 **5,000 Coins**"),
            ("Double XP Ticket", "💰 **7,500 Coins**"),
            ("Boss Raid Ticket", "💰 **15,000 Coins**"),
            ("Marketplace Tax Pass", "💰 **25,000 Coins**")
        ]
    },

    {
        "title": "💎 GEM STORE",
        "description": "Premium rewards purchased using Gems.",
        "fields": [
            ("Phoenix Aura", "💎 **25 Gems**"),
            ("Dragon Aura", "💎 **50 Gems**"),
            ("Cosmic Aura", "💎 **100 Gems**"),
            ("Animated Border", "💎 **250 Gems**")
        ]
    },

    {
        "title": "✨ COSMETICS",
        "description": "Customize your profile.",
        "fields": [
            ("Bronze Theme", "💰 **5,000 Coins**"),
            ("Ancient Temple", "💰 **20,000 Coins**"),
            ("Dragon Kingdom", "💰 **50,000 Coins**"),
            ("Volcano Theme", "💰 **75,000 Coins**"),
            ("Cosmic Theme", "💰 **150,000 Coins**")
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