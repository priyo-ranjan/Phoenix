import discord
from discord.ext import commands

class RulesView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        # We don't store "self.page" here because this View is persistent and shared.
        # Instead, we define the embeds and let the interaction track the state.

    def get_embeds(self):
        color = 0xbb86fc
        
        # --- PAGE 1: THE FOUNDATION ---
        e1 = discord.Embed(
            title="✦ PHOENIX | THE FOUNDATION",
            description=(
                "Welcome to the inner circle. To maintain the energy of this space, "
                "every member is expected to uphold these core standards.\n\n"
                "**01. VIBE CHECK**\nKeep it chill. Respect is the only currency here.\n\n"
                "**02. NO TOXICITY**\nZero tolerance for racism, hate speech, or harassment.\n\n"
                "**03. CLEAN CHATS**\nDon't flood. No emoji vomit or mention spamming.\n\n"
                "**04. DRAMA FREE**\nTake arguments to the DMs. Don't ruin the public vibe.\n\n"
                "**05. USER PRIVACY**\nDon't leak info (doxxing). Respect everyone's identity."
            ),
            color=color
        )
        e1.set_image(url="https://cdn.discordapp.com/attachments/1499252105947386088/1501639529029701833/ay1xeC5qcGc.png?ex=69fcce4a&is=69fb7cca&hm=d1701d63b78300c6d26a65000366545526f7ebf5643ccf2fcf6ef6a65f0cad92&") # Placeholder for an aesthetic banner
        e1.set_footer(text="Section: Core Conduct • Page 1 of 3")

        # --- PAGE 2: THE GUIDELINES ---
        e2 = discord.Embed(
            title="✦ PHOENIX | COMMUNITY GUIDELINES",
            description=(
                "How we keep the machine running smoothly.\n\n"
                "**06. TOPIC RELEVANCY**\nUse the channels for what they were made for.\n\n"
                "**07. ADVERTISING**\nNo unsolicited DMs or server links without staff approval.\n\n"
                "**08. SAFE SPACE**\nNo NSFW, gore, or disturbing content in public channels.\n\n"
                "**09. SCAM PROTECTION**\nDon't click weird links. Reporting scams helps the squad.\n\n"
                "**10. IMPERSONATION**\nDon't pretend to be staff or other high-profile members."
            ),
            color=color
        )
        e2.set_footer(text="Section: Interaction • Page 2 of 3")

        # --- PAGE 3: THE MANDATE ---
        e3 = discord.Embed(
            title="✦ PHOENIX | THE MANDATE",
            description=(
                "The final word on how we operate.\n\n"
                "**11. STAFF AUTHORITY**\nStaff decisions are final. Don't argue with the refs.\n\n"
                "**12. LOOPHOLES**\nTrying to 'bend' the rules is the same as breaking them.\n\n"
                "**13. VOICE ETIQUETTE**\nNo ear-rape, loud music, or toxic yelling in VCs.\n\n"
                "**14. PHOENIX PHILOSOPHY**\nRise together. Shine forever. Be the best version of you.\n\n"
                "**15. EVOLUTION**\nRules can change as we grow. Stay updated."
            ),
            color=color
        )
        e3.set_footer(text="Section: Final Mandate • Page 3 of 3")

        return [e1, e2, e3]

    @discord.ui.button(label="Back", style=discord.ButtonStyle.secondary, custom_id="rules:prev")
    async def prev(self, interaction: discord.Interaction, button: discord.ui.Button):
        # We determine the current page based on the footer of the existing embed
        embeds = self.get_embeds()
        current_page = int(interaction.message.embeds[0].footer.text.split(" ")[2]) - 1
        next_page = (current_page - 1) % len(embeds)
        await interaction.response.edit_message(embed=embeds[next_page])

    @discord.ui.button(label="Next Page", style=discord.ButtonStyle.primary, custom_id="rules:next")
    async def next(self, interaction: discord.Interaction, button: discord.ui.Button):
        embeds = self.get_embeds()
        current_page = int(interaction.message.embeds[0].footer.text.split(" ")[2]) - 1
        next_page = (current_page + 1) % len(embeds)
        await interaction.response.edit_message(embed=embeds[next_page])

class Rules(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # Register the view for persistence across restarts
        self.bot.add_view(RulesView())

    @commands.command(name="rules")
    @commands.has_permissions(administrator=True)
    async def rules(self, ctx):
        """Official deployment of the Phoenix Rules System."""
        await ctx.message.delete()
        
        view = RulesView()
        # Always sends page 1 (index 0) initially
        await ctx.send(embed=view.get_embeds()[0], view=view)

    @rules.error
    async def rules_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("❌ Access Denied. Only **Phoenix Authority** can trigger this.", delete_after=5)

async def setup(bot):
    await bot.add_cog(Rules(bot))