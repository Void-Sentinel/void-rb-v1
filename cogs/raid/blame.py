# STATUS: Complete
import random
import discord
from discord import app_commands
from discord.ext import commands


class Blame(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    @app_commands.command(name="blame", description="Blame a user for a raid")
    @app_commands.describe(user="The user to blame")
    async def blame(self, interaction: discord.Interaction, user: discord.User = None):
        target = user or interaction.user
        await interaction.response.send_message("Blaming.....", ephemeral=True)

        random_time = f"{random.uniform(0.70, 2.70):.2f}s"
        embed = discord.Embed(
            color=14944769,
            title="⚔ Raid Complete!",
            description=(
                f"{target.mention} your raid has been completed with a time of `{random_time}`!\n"
                f"if you are interest in **free premium** u can join the [server](https://discord.gg/Zwa2Jx6vf7)"
            ),
        )
        await interaction.followup.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Blame(bot))
