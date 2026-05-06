import discord
from discord.ext import commands


class RulesView(discord.ui.View):
    def init(self, author):
        super().init(timeout=180)
        self.author = author
        self.page = 0

        self.embeds = [
            self.page_one(),
            self.page_two(),
            self.page_three()
        ]

    def page_one(self):
        embed = discord.Embed(
            title="📜 The Nexus Rules • Page 1/3",
            description=(
                "```yaml\n"
                "Welcome to The Nexus.\n"
                "Please follow all rules below.\n"
                "```"
            ),
            color=0x7b2cbf
        )

        embed.add_field(
            name="1️⃣ Respect Everyone",
            value="No harassment, hate speech, bullying, or personal attacks.",
            inline=False
        )

        embed.add_field(
            name="2️⃣ No Spam",
            value="Avoid message spam, emoji spam, or unnecessary pinging.",
            inline=False
        )

        embed.add_field(
            name="3️⃣ Keep It Civil",
            value="Arguments are fine. Toxicity is not.",
            inline=False
        )

        embed.set_footer(text="Phoenix Rules System")

        return embed

    def page_two(self):
        embed = discord.Embed(
            title="📜 The Nexus Rules • Page 2/3",
            color=0x7b2cbf
        )

        embed.add_field(
            name="4️⃣ No NSFW Content",
            value="NSFW, gore, or disturbing content is prohibited.",
            inline=False
        )

        embed.add_field(
            name="5️⃣ No Advertising",
            value="Do not promote servers, social media, or services without permission.",
            inline=False
        )

        embed.add_field(
            name="6️⃣ Use Correct Channels",
            value="Keep discussions in their appropriate channels.",
            inline=False
        )

        embed.set_footer(text="Phoenix Rules System")

        return embed

    def page_three(self):
        embed = discord.Embed(
            title="📜 The Nexus Rules • Page 3/3",
            color=0x7b2cbf
        )

        embed.add_field(
            name="7️⃣ Follow Discord ToS",
            value="All users must follow Discord's Terms of Service.",
            inline=False
        )

        embed.add_field(
            name="8️⃣ Staff Decisions",
            value="Moderators and admins have the final say in server matters.",
            inline=False
        )

        embed.add_field(
            name="9️⃣ Have Fun",
            value="Enjoy your stay and help build a positive community.",
            inline=False
        )

        embed.set_image(
            url="https://images.unsplash.com/photo-1519681393784-d120267933ba"
        )

        embed.set_footer(text="Welcome to The Nexus 🌌")

        return embed

    @discord.ui.button(label="⬅ Previous", style=discord.ButtonStyle.secondary)
    async def previous_page(self, interaction: discord.Interaction, button: discord.ui.Button):

        if interaction.user != self.author:
            return await interaction.response.send_message(
                "❌ You cannot control someone else's rules menu.",
                ephemeral=True
            )

        self.page -= 1

        if self.page < 0:
            self.page = len(self.embeds) - 1

        await interaction.response.edit_message(
            embed=self.embeds[self.page],
            view=self
        )

    @discord.ui.button(label="Next ➡", style=discord.ButtonStyle.primary)
    async def next_page(self, interaction: discord.Interaction, button: discord.ui.Button):

        if interaction.user != self.author:
            return await interaction.response.send_message(
                "❌ You cannot control someone else's rules menu.",
                ephemeral=True
            )

        self.page += 1

        if self.page >= len(self.embeds):
            self.page = 0

        await interaction.response.edit_message(
            embed=self.embeds[self.page],
            view=self
        )

class Rules(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def rules(self, ctx):

        view = RulesView(ctx.author)

        await ctx.send(
            embed=view.embeds[0],
            view=view
        )

async def setup(bot):
    await bot.add_cog(Rules(bot))