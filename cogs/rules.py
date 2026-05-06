import discord
from discord.ext import commands

class RulesView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        
    def get_pages(self):
        color = 0xbb86fc
        pages = []

        # --- PAGE 1: THE FOUNDATION ---
        e1 = discord.Embed(
            title="✦ PHOENIX | THE FOUNDATION",
            description=(
                "Welcome to the inner circle. To maintain the energy of this space, "
                "every member is expected to uphold these core standards.\n\n"
                "**1. VIBE CHECK**\nKeep it chill. Respect is the only currency here.\n\n"
                "**2. NO TOXICITY**\nZero tolerance for racism, hate speech, or harassment.\n\n"
                "**3. CLEAN CHATS**\nDon't flood. No emoji vomit or mention spamming.\n\n"
                "**4. DRAMA FREE**\nTake arguments to the DMs. Don't ruin the public vibe.\n\n"
                "**5. USER PRIVACY**\nDon't leak info. Respect everyone's identity."
            ),
            color=color
        )
        # SET YOUR IMAGE URL HERE FOR PAGE 1
        e1.set_image(url="https://cdn.discordapp.com/attachments/1499252105947386088/1501639529029701833/ay1xeC5qcGc.png?ex=69fcce4a&is=69fb7cca&hm=d1701d63b78300c6d26a65000366545526f7ebf5643ccf2fcf6ef6a65f0cad92&")
        e1.set_footer(text="Page 1 of 3")
        pages.append(e1)

        # --- PAGE 2: COMMUNITY GUIDELINES ---
        e2 = discord.Embed(
            title="✦ PHOENIX | COMMUNITY GUIDELINES",
            description=(
                "How we keep the machine running smoothly.\n\n"
                "**6. TOPIC RELEVANCY**\nUse the channels for what they were made for.\n\n"
                "**7. ADVERTISING**\nNo unsolicited DMs or server links without approval.\n\n"
                "**8. SAFE SPACE**\nNo NSFW, gore, or disturbing content in public.\n\n"
                "**9. SCAM PROTECTION**\nDon't click weird links. Report suspicious activity.\n\n"
                "**10. IMPERSONATION**\nDon't pretend to be staff or other members."
            ),
            color=color
        )
        # OPTIONAL: You can set a different image for Page 2 here
        e2.set_image(url="https://cdn.discordapp.com/attachments/1499252105947386088/1501646409185624375/aGQtZHAuanBn.png?ex=69fcd4b3&is=69fb8333&hm=03ee1c9c4fe75699cc3e0532337df853167a449ddb55e6b1b53a6705597d4fa6&")
        e2.set_footer(text="Page 2 of 3")
        pages.append(e2)

        # --- PAGE 3: THE MANDATE ---
        e3 = discord.Embed(
            title="✦ PHOENIX | THE MANDATE",
            description=(
                "The final word on how we operate.\n\n"
                "**11. STAFF AUTHORITY**\nStaff decisions are final. Don't argue with the refs.\n\n"
                "**12. LOOPHOLES**\nTrying to 'bend' the rules is the same as breaking them.\n\n"
                "**13. VOICE ETIQUETTE**\nNo ear-rape, loud music, or toxic yelling in VCs.\n\n"
                "**14. PHOENIX PHILOSOPHY**\nRise together. Shine forever.\n\n"
                "**15. EVOLUTION**\nRules can change as we grow. Stay updated."
            ),
            color=color
        )
        # OPTIONAL: You can set a different image for Page 3 here
        e3.set_image(url="https://cdn.discordapp.com/attachments/1499252105947386088/1501645566042443846/cGc.png?ex=69fcd3ea&is=69fb826a&hm=45cba7bb56634b8704243d7c59da18e95e64ecbd7f80983b9c843ef92c35188b&")
        e3.set_footer(text="Page 3 of 3")
        pages.append(e3)

        return pages

    @discord.ui.button(label="Back", style=discord.ButtonStyle.secondary, custom_id="persistent:rules:back")
    async def back_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            pages = self.get_pages()
            current_page = int(interaction.message.embeds[0].footer.text.split(" ")[1]) - 1
            new_index = (current_page - 1) % len(pages)
            await interaction.response.edit_message(embed=pages[new_index])
        except Exception as e:
            print(f"Error in rules back button: {e}")

    @discord.ui.button(label="Next Page", style=discord.ButtonStyle.primary, custom_id="persistent:rules:next")
    async def next_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            pages = self.get_pages()
            current_page = int(interaction.message.embeds[0].footer.text.split(" ")[1]) - 1
            new_index = (current_page + 1) % len(pages)
            await interaction.response.edit_message(embed=pages[new_index])
        except Exception as e:
            print(f"Error in rules next button: {e}")

class Rules(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # Registers view globally for persistence
        self.bot.add_view(RulesView())

    @commands.command(name="rules")
    @commands.has_permissions(administrator=True)
    async def rules(self, ctx):
        await ctx.message.delete()
        view = RulesView()
        await ctx.send(embed=view.get_pages()[0], view=view)

async def setup(bot):
    await bot.add_cog(Rules(bot))