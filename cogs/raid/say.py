# STATUS: Complete
import discord
from discord import app_commands
from discord.ext import commands


class Say(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    @app_commands.command(name="say", description="Make the bot say something")
    @app_commands.describe(message="The message to say")
    async def say(self, interaction: discord.Interaction, message: str):
        await interaction.response.send_message("Saying...", ephemeral=True)
        await interaction.followup.send(message)


async def setup(bot):
    await bot.add_cog(Say(bot))
