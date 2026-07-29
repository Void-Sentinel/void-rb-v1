import discord
from discord import app_commands
from discord.ext import commands


class BotInfo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    @app_commands.command(name="botinfo", description="Bot info - coming soon")
    async def botinfo(self, interaction: discord.Interaction):
        await interaction.response.send_message("Coming soon!", ephemeral=True)


async def setup(bot):
    await bot.add_cog(BotInfo(bot))
