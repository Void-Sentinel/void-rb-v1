import aiosqlite
import discord
from pathlib import Path
from discord import app_commands
from discord.ext import commands
from discord.ui import View, Button, Modal, TextInput


DB_PATH = Path(__file__).parent.parent.parent / "data" / "presets.db"


class PresetDB:
    def __init__(self, db_path=DB_PATH):
        self.db_path = db_path

    async def init(self):
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(
                "CREATE TABLE IF NOT EXISTS presets (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER NOT NULL, name TEXT NOT NULL, message TEXT NOT NULL)"
            )
            await db.commit()

    async def add_preset(self, user_id: int, name: str, message: str):
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(
                "INSERT INTO presets (user_id, name, message) VALUES (?, ?, ?)",
                (user_id, name, message),
            )
            await db.commit()

    async def get_user_presets(self, user_id: int):
        async with aiosqlite.connect(self.db_path) as db:
            async with db.execute(
                "SELECT id, name, message FROM presets WHERE user_id = ?", (user_id,)
            ) as cursor:
                rows = await cursor.fetchall()
                return [{"id": row[0], "name": row[1], "message": row[2]} for row in rows]

    async def get_preset(self, user_id: int, name: str):
        async with aiosqlite.connect(self.db_path) as db:
            async with db.execute(
                "SELECT message FROM presets WHERE user_id = ? AND name = ?", (user_id, name)
            ) as cursor:
                row = await cursor.fetchone()
                return row[0] if row else None

    async def delete_preset(self, user_id: int, preset_id: int):
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(
                "DELETE FROM presets WHERE id = ? AND user_id = ?", (preset_id, user_id)
            )
            await db.commit()


class CreateModal(Modal, title="Create Preset"):
    title_input = TextInput(label="Title", placeholder="Preset name")
    message_input = TextInput(label="Message", placeholder="Your custom message", style=discord.TextStyle.paragraph)

    def __init__(self, db: PresetDB, user_id: int):
        super().__init__()
        self.db = db
        self.user_id = user_id

    async def on_submit(self, interaction: discord.Interaction):
        name = self.title_input.value.strip()
        message = self.message_input.value.strip()
        if not name or not message:
            await interaction.response.send_message("Both fields are required.", ephemeral=True)
            return
        await self.db.add_preset(self.user_id, name, message)
        await interaction.response.send_message(f"Preset `{name}` created.", ephemeral=True)


class PresetView(View):
    def __init__(self, db: PresetDB, user_id: int):
        super().__init__(timeout=None)
        self.db = db
        self.user_id = user_id

    @discord.ui.button(label="Create", style=discord.ButtonStyle.success)
    async def create_button(self, interaction: discord.Interaction, button: Button):
        await interaction.response.send_modal(CreateModal(self.db, self.user_id))

    @discord.ui.button(label="List", style=discord.ButtonStyle.primary)
    async def list_button(self, interaction: discord.Interaction, button: Button):
        presets = await self.db.get_user_presets(self.user_id)
        if not presets:
            await interaction.response.send_message("You have no presets.", ephemeral=True)
            return
        embed = discord.Embed(title="Your Presets", color=discord.Color.blue())
        for p in presets:
            embed.add_field(name=p["name"], value=f"ID: {p['id']}", inline=False)
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @discord.ui.button(label="Delete", style=discord.ButtonStyle.danger)
    async def delete_button(self, interaction: discord.Interaction, button: Button):
        presets = await self.db.get_user_presets(self.user_id)
        if not presets:
            await interaction.response.send_message("You have no presets to delete.", ephemeral=True)
            return

        view = View(timeout=60)
        for p in presets:
            def make_callback(pid, pname):
                async def callback(interaction: discord.Interaction):
                    await self.db.delete_preset(self.user_id, pid)
                    await interaction.response.send_message(f"Deleted preset `{pname}`.", ephemeral=True)
                    view.stop()
                return callback

            btn = Button(label=f"{p['name']} (ID: {p['id']})", style=discord.ButtonStyle.danger)
            btn.callback = make_callback(p["id"], p["name"])
            view.add_item(btn)

        await interaction.response.send_message("Select a preset to delete:", view=view, ephemeral=True)


class Custom(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = PresetDB()

    async def cog_load(self):
        await self.db.init()

    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    @app_commands.command(name="custom-msg", description="[PREMIUM] Set a custom message.")
    async def custom_msg(self, interaction: discord.Interaction):
        view = PresetView(self.db, interaction.user.id)
        embed = discord.Embed(
            title="Custom Message Manager",
            description="Manage your raid message presets",
        )
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)


async def setup(bot):
    await bot.add_cog(Custom(bot))
