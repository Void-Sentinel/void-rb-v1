import discord
from discord import app_commands
from discord.ext import commands


class BotInfo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    @app_commands.command(name="botinfo", description="Shows information about the bot")
    async def botinfo(self, interaction: discord.Interaction):
        cogs_loaded = ", ".join(sorted(self.bot.cogs.keys())) or "None"
        commands_count = len(self.bot.tree.get_commands())
        created_ts = int(self.bot.user.created_at.timestamp())

        embed = discord.Embed(
            description=(
                "**Void Spam Bot**\n"
                f"-# Version 2.0.5\n"
                f"-# **Cogs Loaded:** {cogs_loaded}\n"
                f"-# **Bot Created on <t:{created_ts}>**\n"
                f"-# **Commands: `{commands_count}`**\n"
                "-# **Developer:** Voby7\n"
            ),
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)


async def setup(bot):
    await bot.add_cog(BotInfo(bot))
