# STATUS: Complete
import asyncio
import discord

from discord import app_commands
from discord.ext import commands
from discord.ui import View, Button

import aiohttp

from core.config import RAID_MESSAGE, TOKEN
from core.utils import send_message_http


class Raid(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.session: aiohttp.ClientSession | None = None

    async def cog_load(self):
        self.session = aiohttp.ClientSession()

    async def cog_unload(self):
        if self.session and not self.session.closed:
            await self.session.close()

    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    @app_commands.command(name="r4id", description="if ykyk")
    async def raid(self, interaction: discord.Interaction):
        view = RaidView(self.bot, self.session)
        await interaction.response.send_message("Click the button to raid!", view=view, ephemeral=True)


class RaidView(View):
    def __init__(self, bot, session: aiohttp.ClientSession):
        super().__init__()
        self.bot = bot
        self.session = session

    @discord.ui.button(label="Raid", style=discord.ButtonStyle.danger)
    async def raid_button(self, interaction: discord.Interaction, button: Button):
        await interaction.response.defer()

        application_id = interaction.client.user.id
        interaction_token = interaction.token

        tasks = []
        for _ in range(5):
            tasks.append(
                send_message_http(self.session, application_id, interaction_token, RAID_MESSAGE)
            )
        results = await asyncio.gather(*tasks, return_exceptions=True)
        for r in results:
            if isinstance(r, Exception):
                print(f"Raid send failed: {r}")
            elif r >= 400:
                print(f"Raid send returned status {r}")



async def setup(bot):
    await bot.add_cog(Raid(bot))
