import discord
from discord.ext import commands
from discord.ui import View, Button


HELP_PAGES = [
    {
        "title": "🔥 Phoenix Help Center",
        "description": (
            "**Welcome to Phoenix.**\n"
            "A multipurpose Discord bot featuring AI, Economy, Gambling, "
            "Leveling, Trading, Reputation and Moderation systems.\n\n"
            "Use the buttons below to browse categories."
        ),
        "fields": [
            ("🤖 AI", "`1 Command`"),
            ("🥳 Fun", "`4 Commands`"),
            ("📈 Leveling", "`2 Commands`"),
            ("🎰 Gambling", "`2 Commands`"),
            ("💸 Trading", "`5 Commands`"),
            ("💰 Economy", "`3 Commands`"),
            ("💎 Reputation", "`2 Commands`"),
            ("🧠 Memory", "`3 Commands`"),
            ("🛡 Moderation", "`5 Commands`")
        ]
    },

    {
        "title": "🤖 AI Commands",
        "description": "Artificial Intelligence Commands",
        "fields": [
            (
                "① !ai <prompt>",
                "➜ Ask Phoenix anything using AI."
            )
        ]
    },

    {
        "title": "🥳 Fun Commands",
        "description": "Entertainment & Utility Commands",
        "fields": [
            (
                "① !roast",
                "➜ Roast a member."
            ),
            (
                "② !say",
                "➜ Make Phoenix say something."
            ),
            (
                "③ !ping",
                "➜ View bot latency."
            ),
            (
                "④ !hello",
                "➜ Receive a greeting."
            )
        ]
    },

    {
        "title": "📈 Leveling Commands",
        "description": "XP, Activity & Ranking",
        "fields": [
            (
                "① !rank",
                "➜ View your current rank."
            ),
            (
                "② !rank @user",
                "➜ View another user's rank."
            ),
            (
                "③ !top",
                "➜ View the server's top users."
            )
        ]
    },

    {
        "title": "🎰 Gambling Commands",
        "description": "High Risk. High Reward.",
        "fields": [
            (
                "① !flip <amount>",
                "➜ Coinflip your wager."
            ),
            (
                "② !jackpot",
                "➜ Attempt to win the jackpot."
            )
        ]
    },

    {
        "title": "💸 Trading Commands",
        "description": "Trade Coins, Gems & Crates",
        "fields": [
            (
                "① !trade @user",
                "➜ Start a trade session."
            ),
            (
                "② !accept",
                "➜ Accept a pending trade."
            ),
            (
                "③ !decline",
                "➜ Decline a pending trade."
            ),
            (
                "④ !offer <amount> <item>",
                "➜ Add items to the trade."
            ),
            (
                "⑤ !remove <amount> <item>",
                "➜ Remove items from the trade."
            )
        ]
    },

    {
        "title": "💰 Economy Commands",
        "description": "Manage Your Wealth",
        "fields": [
            (
                "① !balance / !bal",
                "➜ Check your wallet."
            ),
            (
                "② !daily",
                "➜ Claim daily rewards."
            ),
            (
                "③ !opencrate <amount>",
                "➜ Open crates for rewards."
            )
        ]
    },

    {
        "title": "💎 Reputation Commands",
        "description": "Community Reputation System",
        "fields": [
            (
                "① !rep @user",
                "➜ Give reputation."
            ),
            (
                "② !reps @user",
                "➜ View reputation."
            )
        ]
    },

    {
        "title": "🧠 Memory Commands",
        "description": "Phoenix Memory System",
        "fields": [
            (
                "① !remember <key> <memory>",
                "➜ Save a memory."
            ),
            (
                "② !memories @user",
                "➜ View saved memories."
            ),
            (
                "③ !forget <key>",
                "➜ Delete a memory."
            )
        ]
    },

    {
        "title": "🛡 Moderation Commands",
        "description": "Server Management Tools",
        "fields": [
            (
                "① !kick",
                "➜ Kick a member."
            ),
            (
                "② !mute",
                "➜ Mute a member."
            ),
            (
                "③ !unmute",
                "➜ Unmute a member."
            ),
            (
                "④ !ban",
                "➜ Ban a member."
            ),
            (
                "⑤ !purge <amount>",
                "➜ Bulk delete messages."
            )
        ]
    }
]


class HelpView(View):
    def __init__(self, bot):
        super().__init__(timeout=180)
        self.bot = bot
        self.page = 0

    def create_embed(self):

        data = HELP_PAGES[self.page]

        embed = discord.Embed(
            title=data["title"],
            description=data["description"],
            color=0xFF6B00
        )

        for name, value in data["fields"]:
            embed.add_field(
                name=name,
                value=value,
                inline=False
            )

        embed.set_thumbnail(
            url=self.bot.user.display_avatar.url
        )

        embed.set_footer(
            text=f"Phoenix Bot • Page {self.page + 1}/{len(HELP_PAGES)}"
        )

        return embed

    @discord.ui.button(
        label="◀ Previous",
        style=discord.ButtonStyle.secondary
    )
    async def previous(self, interaction: discord.Interaction, button: Button):

        if self.page > 0:
            self.page -= 1

        await interaction.response.edit_message(
            embed=self.create_embed(),
            view=self
        )

    @discord.ui.button(
      label="🏠 Home",
      style=discord.ButtonStyle.success
  ) 
    async def home(self, interaction: discord.Interaction, button: Button):

      self.page = 0

      await interaction.response.edit_message(
          embed=self.create_embed(),
          view=self
    )
    
    @discord.ui.button(
        label="▶ Next",
        style=discord.ButtonStyle.primary
    )
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

        view = HelpView(self.bot)

        await ctx.send(
            embed=view.create_embed(),
            view=view
        )


async def setup(bot):
    await bot.add_cog(Help(bot))