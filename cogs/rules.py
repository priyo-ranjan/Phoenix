import discord
from discord.ext import commands

class RulesView(discord.ui.View):
    """The interactive button view for the rules pages."""
    def __init__(self):
        # timeout=None is required for persistent buttons
        super().__init__(timeout=None)
        self.page = 0
        self.embeds = self._create_embeds()

    def _create_embeds(self):
        """Helper method to define your rules pages."""
        color = 0xbb86fc
        
        # PAGE 1: Core Rules
        e1 = discord.Embed(
            title="✦ PHOENIX SERVER RULES",
            description="Welcome to the server.\nKeep the vibe clean, chill, and respectful.",
            color=color
        )
        e1.add_field(name="⚡ Respect Everyone", value="No harassment, racism, or toxic behavior.", inline=False)
        e1.add_field(name="🎭 No Drama", value="Avoid unnecessary arguments and attention-seeking.", inline=False)
        e1.add_field(name="🚫 No Spam", value="Do not flood chats, spam emojis, or abuse mentions.", inline=False)
        e1.set_footer(text="Page 1 / 3 • Phoenix Rules System")

        # PAGE 2: Guidelines
        e2 = discord.Embed(
            title="✦ COMMUNITY GUIDELINES",
            description="This server is built for good vibes and quality conversations.",
            color=color
        )
        e2.add_field(name="📢 Keep Channels Clean", value="Use channels for their intended purpose.", inline=False)
        e2.add_field(name="🔞 No NSFW Content", value="Explicit or disturbing content is strictly forbidden.", inline=False)
        e2.add_field(name="🛡️ No Scams", value="Advertising scams, malware, or phishing = instant ban.", inline=False)
        e2.set_footer(text="Page 2 / 3 • Phoenix Rules System")

        # PAGE 3: Final Notes
        e3 = discord.Embed(
            title="✦ FINAL NOTES",
            description="Help us maintain the aesthetic and energy of the server.",
            color=color
        )
        e3.add_field(name="👑 Staff Decisions", value="Respect moderator decisions and avoid back-seat modding.", inline=False)
        e3.add_field(name="🌌 Enjoy Your Stay", value="Make friends, have fun, and grow with the community.", inline=False)
        e3.add_field(name="🔥 Phoenix Philosophy", value="Rise together. Shine forever.", inline=False)
        e3.set_footer(text="Page 3 / 3 • Phoenix Rules System")

        return [e1, e2, e3]

    @discord.ui.button(label="⬅ Previous", style=discord.ButtonStyle.secondary, custom_id="rules:prev")
    async def previous_page(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.page = (self.page - 1) % len(self.embeds)
        await interaction.response.edit_message(embed=self.embeds[self.page], view=self)

    @discord.ui.button(label="Next ➜", style=discord.ButtonStyle.primary, custom_id="rules:next")
    async def next_page(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.page = (self.page + 1) % len(self.embeds)
        await interaction.response.edit_message(embed=self.embeds[self.page], view=self)

class Rules(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # This registers the view so buttons work after bot restarts
        self.bot.add_view(RulesView())

    @commands.command(name="rules")
    @commands.has_permissions(administrator=True)
    async def rules(self, ctx):
        """Deploys the multi-page rules embed."""
        # Deletes your "!rules" command to keep the channel clean
        await ctx.message.delete()
        
        view = RulesView()
        await ctx.send(embed=view.embeds[0], view=view)

    @rules.error
    async def rules_error(self, ctx, error):
        """Handles cases where non-admins try to use the command."""
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("❌ Only **Phoenix Administrators** can deploy the rules.", delete_after=5)

async def setup(bot):
    await bot.add_cog(Rules(bot))