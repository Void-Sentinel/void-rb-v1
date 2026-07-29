# STATUS: Complete
import asyncio
import discord

from discord import app_commands
from discord.ext import commands
from discord.ui import View, Button
import aiohttp
from core.utils import send_message_http, delete_message_http


class Ghostping(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.session: aiohttp.ClientSession | None = None

    async def cog_load(self):
        self.session = aiohttp.ClientSession()

    async def cog_unload(self):
        if self.session and not self.session.closed:
            await self.session.close()

    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    @app_commands.command(name="ghostping", description="Ghostping someone")
    @app_commands.describe(user="The user to ghostping")
    async def ghostping(self, interaction: discord.Interaction, user: discord.User = None):
        target = user or interaction.user
        view = GhostpingView(self.bot, self.session, target)
        await interaction.response.send_message("Choose a ghostping option:", view=view, ephemeral=True)


class GhostpingView(View):
    def __init__(self, bot, session: aiohttp.ClientSession, target: discord.User):
        super().__init__()
        self.bot = bot
        self.session = session
        self.target = target

    @discord.ui.button(label="Ghostping Everyone", style=discord.ButtonStyle.danger)
    async def everyone_button(self, interaction: discord.Interaction, button: Button):
        await interaction.response.defer()
        await self._send_and_delete(interaction, "@everyone")

    @discord.ui.button(label="Ghostping User", style=discord.ButtonStyle.danger)
    async def user_button(self, interaction: discord.Interaction, button: Button):
        await interaction.response.defer()
        content = f"<@{self.target.id}>"
        await self._send_and_delete(interaction, content)

    async def _send_and_delete(self, interaction: discord.Interaction, content: str):
        app_id = interaction.client.user.id
        token = interaction.token

        status, data = await send_message_http(self.session, app_id, token, content)
        message_id = data.get("id") if isinstance(data, dict) else None

        if message_id:
            asyncio.create_task(
                delete_message_http(self.session, app_id, token, message_id)
            )


async def setup(bot):
    await bot.add_cog(Ghostping(bot))
