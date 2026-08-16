import discord
from discord.ext import commands
from discord.ui import View, Button


INVENTORY_PAGES = [

    {
        "title": "🎒 PHOENIX INVENTORY",
        "description": (
            "```yaml\n"
            "Welcome to your personal storage.\n"
            "Browse your categories below.\n"
            "```"
        ),
        "fields": [

            ("🥚 __EGGS__", "Stored creature eggs"),
            ("🎒 __UTILITIES__", "Tools and equipment"),
            ("📦 __CONSUMABLES__", "One-time use items"),
            ("🎟 __TICKETS__", "Special event passes"),
            ("💎 __GEMS__", "Premium currency"),
            ("✨ __COSMETICS__", "Profile customization"),
            ("🐾 __CREATURES__", "Your creature collection")

        ]
    },

    {
        "title": "🥚 EGG STORAGE",
        "description": "All creature eggs currently owned.",
        "fields": [

            (
                "🥚 Common Egg",
                "Perfect for beginners.\nOwned: **x0**\n\n"
            ),

            (
                "🦴 Extinct Egg",
                "Contains creatures from the Extinct Realm.\nOwned: **x0**\n\n"
            ),

            (
                "🐉 Dragon Egg",
                "Contains creatures from the Dragon Realm.\nOwned: **x0**\n\n"
            ),

            (
                "🔥 Mythic Egg",
                "Contains mythical creatures.\nOwned: **x0**\n\n"
            ),

            (
                "🌌 Cosmic Egg",
                "Contains ultra rare creatures.\nOwned: **x0**\n\n"
            )

        ]
    },

    {
        "title": "🎒 UTILITIES",
        "description": "Useful tools for creature hunting.",
        "fields": [

            (
                "🎯 Hunter's Net",
                "Improves catch chance.\nOwned: **x0**\n\n"
            ),

            (
                "✨ Golden Net",
                "Premium capture tool.\nOwned: **x0**\n\n"
            ),

            (
                "🧭 Ancient Compass",
                "Find rare spawns.\nOwned: **x0**\n\n"
            ),

            (
                "🔍 Beast Tracker",
                "Track nearby creatures.\nOwned: **x0**\n\n"
            )

        ]
    },

    {
        "title": "📦 CONSUMABLES",
        "description": "Temporary use items.",
        "fields": [

            (
                "📜 Small XP Scroll",
                "Grants creature XP.\nOwned: **x0**\n\n"
            ),

            (
                "📖 Medium XP Scroll",
                "Grants more creature XP.\nOwned: **x0**\n\n"
            ),

            (
                "📚 Large XP Scroll",
                "Huge XP boost.\nOwned: **x0**\n\n"
            ),

            (
                "💎 Revive Crystal",
                "Revive a defeated creature.\nOwned: **x0**\n\n"
            )

        ]
    },

    {
        "title": "🎟 TICKETS",
        "description": "Special passes and event items.",
        "fields": [

            (
                "🎟 Rare Spawn Ticket",
                "Boost rare spawns.\nOwned: **x0**\n\n"
            ),

            (
                "⚡ Double XP Ticket",
                "Double XP gains.\nOwned: **x0**\n\n"
            ),

            (
                "👹 Boss Raid Ticket",
                "Access special bosses.\nOwned: **x0**\n\n"
            )

        ]
    },

    {
        "title": "💎 GEM VAULT",
        "description": "Premium currency information.",
        "fields": [

            ("💎 Current Gems", "**0**"),
            ("📈 Lifetime Earned", "**0**"),
            ("📉 Lifetime Spent", "**0**")

        ]
    },

    {
        "title": "✨ COSMETICS",
        "description": "Owned profile cosmetics.",
        "fields": [

            ("🥉 Bronze Theme", "Owned: ❌"),
            ("🏛 Ancient Temple", "Owned: ❌"),
            ("🐉 Dragon Kingdom", "Owned: ❌"),
            ("🌋 Volcano Theme", "Owned: ❌"),
            ("🌌 Cosmic Theme", "Owned: ❌")

        ]
    },

    {
        "title": "🐾 CREATURE STORAGE",
        "description": "Your creature collection.",
        "fields": [

            ("Common Creatures", "**0**"),
            ("Rare Creatures", "**0**"),
            ("Epic Creatures", "**0**"),
            ("Legendary Creatures", "**0**"),
            ("Mythic Creatures", "**0**")

        ]
    }

]


class InventoryView(View):

    def __init__(self):
        super().__init__(timeout=180)
        self.page = 0

    def create_embed(self):

        data = INVENTORY_PAGES[self.page]

        embed = discord.Embed(
            title=data["title"],
            description=data["description"],
            color=0x3498DB
        )

        for name, value in data["fields"]:
            embed.add_field(
                name=name,
                value=value,
                inline=False
            )

        embed.set_footer(
            text=f"Phoenix Inventory • Page {self.page + 1}/{len(INVENTORY_PAGES)}"
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

        if self.page < len(INVENTORY_PAGES) - 1:
            self.page += 1

        await interaction.response.edit_message(
            embed=self.create_embed(),
            view=self
        )


class Inventory(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["inv"])
    async def inventory(self, ctx):

        view = InventoryView()

        await ctx.send(
            embed=view.create_embed(),
            view=view
        )


async def setup(bot):
    await bot.add_cog(Inventory(bot))