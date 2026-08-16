import discord
from discord.ext import commands
from discord.ui import View, Button


HELP_PAGES = [
    {
        "title": "🔥 Phoenix Help Center",
        "description": "Welcome to Phoenix Bot.\nUse the buttons below to browse command categories.",
        "fields": [
            ("🤖 AI", "1 command"),
            ("🥳 Fun", "4 commands"),
            ("📈 Leveling", "2 commands"),
            ("🎰 Gambling", "2 commands"),
            ("💰 Economy", "3 commands"),
            ("💎 Reputation", "2 commands"),
            ("🧠 Memory", "3 commands"),
            ("🛡 Moderation", "5 commands")
        ]
    },

    {
        "title": "🤖 AI Commands",
        "description": "AI powered commands.",
        "fields": [
            ("!ai <prompt>", "Ask Phoenix AI anything.")
        ]
    },

    {
        "title": "🥳 Fun Commands",
        "description": "Fun and entertainment commands.",
        "fields": [
            ("!roast", "Roast a user."),
            ("!say", "Make Phoenix say something."),
            ("!ping", "Check bot latency."),
            ("!hello", "Say hello.")
        ]
    },

    {
        "title": "📈 Leveling Commands",
        "description": "XP and ranking system.",
        "fields": [
            ("!rank", "View your rank."),
            ("!rank @user", "View another user's rank.")
        ]
    },

    {
        "title": "🎰 Gambling Commands",
        "description": "Risk it all.",
        "fields": [
            ("!flip <amount>", "Coinflip your coins."),
            ("!jackpot", "Try your luck.")
        ]
    },

    {
        "title": "💰 Economy Commands",
        "description": "Earn and spend coins.",
        "fields": [
            ("!balance / !bal", "Check your balance."),
            ("!daily", "Claim daily reward."),
            ("!opencrate <amount>", "Open crates.")
        ]
    },

    {
        "title": "💎 Reputation Commands",
        "description": "Community reputation system.",
        "fields": [
            ("!rep @user", "Give reputation."),
            ("!reps @user", "Check reputation.")
        ]
    },

    {
        "title": "🧠 Memory Commands",
        "description": "Store memories.",
        "fields": [
            ("!remember <key> <memory>", "Save memory."),
            ("!memories @user", "View memories."),
            ("!forget <key>", "Delete memory.")
        ]
    },

    {
        "title": "🛡 Moderation Commands",
        "description": "Server management commands.",
        "fields": [
            ("!kick", "Kick member."),
            ("!mute", "Mute member."),
            ("!unmute", "Unmute member."),
            ("!ban", "Ban member."),
            ("!purge <amount>", "Delete messages.")
        ]
    }
]


class HelpView(View):
    def __init__(self):
        super().__init__(timeout=120)
        self.page = 0

    def create_embed(self):

        data = HELP_PAGES[self.page]

        embed = discord.Embed(
            title=data["title"],
            description=data["description"],
            color=discord.Color.orange()
        )

        for name, value in data["fields"]:
            embed.add_field(
                name=name,
                value=value,
                inline=False
            )

        embed.set_footer(
            text=f"Phoenix Bot • Page {self.page + 1}/{len(HELP_PAGES)}"
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

    @discord.ui.button(label="▶ Next", style=discord.ButtonStyle.primary)
    async def next(self, interaction: discord.Interaction, button: Button):

        if self.page < len(HELP_PAGES) - 1:
            self.page += 1

        await interaction.response.edit_message(
            embed=self.create_embed(),
            view=self
        )


class Help(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def help(self, ctx):

        view = HelpView()

        await ctx.send(
            embed=view.create_embed(),
            view=view
        )


async def setup(bot):
    await bot.add_cog(Help(bot))