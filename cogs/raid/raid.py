# STATUS: Complete
import asyncio
import aiosqlite
import discord
from pathlib import Path
from discord import app_commands
from discord.ext import commands
from discord.ui import View, Button

import aiohttp

from core.config import RAID_MESSAGE, TOKEN
from core.utils import send_message_http


DB_PATH = Path(__file__).parent.parent.parent / "data" / "presets.db"


class Raid(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.session: aiohttp.ClientSession | None = None

    async def cog_load(self):
        self.session = aiohttp.ClientSession()
        DB_PATH.parent.mkdir(parents=True, exist_ok=True)
        async with aiosqlite.connect(DB_PATH) as db:
            await db.execute(
                "CREATE TABLE IF NOT EXISTS presets (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER NOT NULL, name TEXT NOT NULL, message TEXT NOT NULL)"
            )
            await db.commit()

    async def cog_unload(self):
        if self.session and not self.session.closed:
            await self.session.close()

    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    @app_commands.command(name="r4id", description="if ykyk")
    @app_commands.describe(preset="Name of your custom preset message to use")
    async def raid(self, interaction: discord.Interaction, preset: str | None = None):
        message = RAID_MESSAGE
        if preset:
            async with aiosqlite.connect(DB_PATH) as db:
                async with db.execute(
                    "SELECT message FROM presets WHERE user_id = ? AND name = ?", (interaction.user.id, preset)
                ) as cursor:
                    row = await cursor.fetchone()
                    if row:
                        message = row[0]
                    else:
                        await interaction.response.send_message(f"Preset `{preset}` not found.", ephemeral=True)
                        return

        view = RaidView(self.bot, self.session, message)
        await interaction.response.send_message("Click the button to raid!", view=view, ephemeral=True)


class RaidView(View):
    def __init__(self, bot, session: aiohttp.ClientSession, message: str):
        super().__init__()
        self.bot = bot
        self.session = session
        self.message = message

    @discord.ui.button(label="Raid", style=discord.ButtonStyle.danger)
    async def raid_button(self, interaction: discord.Interaction, button: Button):
        await interaction.response.defer()

        application_id = interaction.client.user.id
        interaction_token = interaction.token

        tasks = []
        for _ in range(5):
            tasks.append(
                send_message_http(self.session, application_id, interaction_token, self.message)
            )
        results = await asyncio.gather(*tasks, return_exceptions=True)
        for r in results:
            if isinstance(r, Exception):
                print(f"Raid send failed: {r}")
            elif isinstance(r, tuple):
                status, data = r
                if status >= 400:
                    print(f"Raid send returned status {status}: {data}")


async def setup(bot):
    await bot.add_cog(Raid(bot))
