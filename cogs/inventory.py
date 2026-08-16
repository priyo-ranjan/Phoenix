from operator import inv

import discord
from discord.ext import commands
from discord.ui import View, Button
import database


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

    def __init__(self, inventory):
        super().__init__(timeout=180)
        self.page = 0
        self.inv = {
            item_id: qty for item_id, qty in inventory
        }

    def create_embed(self):

        data = INVENTORY_PAGES[self.page]

    # ======================
    # EGGS PAGE
    # ======================

        if self.page == 1:

            data = {
                "title": "🥚 EGG STORAGE",
                "description": "All creature eggs currently owned.",
                "fields": [

                (
                    "🥚 Common Egg",
                    f"Perfect for beginners.\nOwned: **x{self.inv.get('common_egg', 0)}**"
                ),

                (
                    "🦴 Extinct Egg",
                    f"Contains creatures from the Extinct Realm.\nOwned: **x{self.inv.get('extinct_egg', 0)}**"
                ),

                (
                    "🐉 Dragon Egg",
                    f"Contains creatures from the Dragon Realm.\nOwned: **x{self.inv.get('dragon_egg', 0)}**"
                ),

                (
                    "🔥 Mythic Egg",
                    f"Contains mythical creatures.\nOwned: **x{self.inv.get('mythic_egg', 0)}**"
                ),

                (
                    "🌌 Cosmic Egg",
                    f"Contains ultra rare creatures.\nOwned: **x{self.inv.get('cosmic_egg', 0)}**"
                )

            ]
        }

    # ======================
    # UTILITIES PAGE
    # ======================

        elif self.page == 2:

            data = {
                "title": "🎒 UTILITIES",
                "description": "Useful tools for creature hunting.",
                "fields": [

                (
                    "🎯 Hunter's Net",
                    f"Improves catch chance.\nOwned: **x{self.inv.get('hunters_net', 0)}**"
                ),

                (
                    "✨ Golden Net",
                    f"Premium capture tool.\nOwned: **x{self.inv.get('golden_net', 0)}**"
                ),

                (
                    "🧭 Ancient Compass",
                    f"Find rare spawns.\nOwned: **x{self.inv.get('ancient_compass', 0)}**"
                ),

                (
                    "🔍 Beast Tracker",
                    f"Track nearby creatures.\nOwned: **x{self.inv.get('beast_tracker', 0)}**"
                )

            ]
        }

        elif self.page == 3:

            data = {
                "title": "📦 CONSUMABLES",
                "description": "Temporary use items.",
                "fields": [

            (
                "📜 Small XP Scroll",
                f"Grants creature XP.\nOwned: **x{self.inv.get('small_xp_scroll', 0)}**"
            ),

            (
                "📖 Medium XP Scroll",
                f"Grants more creature XP.\nOwned: **x{self.inv.get('medium_xp_scroll', 0)}**"
            ),

            (
                "📚 Large XP Scroll",
                f"Huge XP boost.\nOwned: **x{self.inv.get('large_xp_scroll', 0)}**"
            ),

            (
                "💎 Revive Crystal",
                f"Revive a defeated creature.\nOwned: **x{self.inv.get('revive_crystal', 0)}**"
            )

        ]
    }
        elif self.page == 4:

            data = {
                "title": "🎟 TICKETS",
                "description": "Special passes and event items.",
                "fields": [

            (
                "🎟 Rare Spawn Ticket",
                f"Boost rare spawns.\nOwned: **x{self.inv.get('rare_spawn_ticket', 0)}**"
            ),

            (
                "⚡ Double XP Ticket",
                f"Double XP gains.\nOwned: **x{self.inv.get('double_xp_ticket', 0)}**"
            ),

            (
                "👹 Boss Raid Ticket",
                f"Access special bosses.\nOwned: **x{self.inv.get('boss_raid_ticket', 0)}**"
            )

        ]
    }
        elif self.page == 5:
            data = {
                "title": "💎 GEM VAULT",
                "description": "Premium currency information.",
                "fields": [

            (
                "💎 Current Gems",
                f"**{self.inv.get('gems', 0)}**"
            ),

            (
                "📈 Lifetime Earned",
                "Coming Soon"
            ),

            (
                "📉 Lifetime Spent",
                "Coming Soon"
            )

        ]
    }
        elif self.page == 6:

            data = {
            "title": "✨ COSMETICS",
            "description": "Owned profile cosmetics.",
            "fields": [

            (
                "🥉 Bronze Theme",
                f"Owned: {'✅' if self.inv.get('bronze_theme', 0) > 0 else '❌'}"
            ),

            (
                "🏛 Ancient Temple",
                f"Owned: {'✅' if self.inv.get('ancient_temple_theme', 0) > 0 else '❌'}"
            ),

            (
                "🐉 Dragon Kingdom",
                f"Owned: {'✅' if self.inv.get('dragon_kingdom_theme', 0) > 0 else '❌'}"
            ),

            (
                "🌋 Volcano Theme",
                f"Owned: {'✅' if self.inv.get('volcano_theme', 0) > 0 else '❌'}"
            ),

            (
                "🌌 Cosmic Theme",
                f"Owned: {'✅' if self.inv.get('cosmic_theme', 0) > 0 else '❌'}"
            )

        ]
    }
        elif self.page == 7:
            data = {
                "title": "🐾 CREATURE STORAGE",
                "description": "Your creature collection.",
                "fields": [

            (
                "Common Creatures",
                f"**{self.inv.get('common_creature', 0)}**"
            ),

            (
                "Rare Creatures",
                f"**{self.inv.get('rare_creature', 0)}**"
            ),

            (
                "Epic Creatures",
                f"**{self.inv.get('epic_creature', 0)}**"
            ),

            (
                "Legendary Creatures",
                f"**{self.inv.get('legendary_creature', 0)}**"
            ),

            (
                "Mythic Creatures",
                f"**{self.inv.get('mythic_creature', 0)}**"
            )

        ]
    }
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

    @commands.command()
    async def debuginv(self, ctx):
        inv = await database.get_inventory(ctx.author.id)
        await ctx.send(f"{inv}")

    @commands.command(aliases=["inv"])
    async def inventory(self, ctx):

        inv = await database.get_inventory(ctx.author.id)

        view = InventoryView(inv)

        await ctx.send(
            embed=view.create_embed(),
            view=view
    )

    
        
async def setup(bot):
    await bot.add_cog(Inventory(bot))