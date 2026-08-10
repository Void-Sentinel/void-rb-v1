import discord
from discord.ext import commands
import traceback
import sys
import pkgutil
from core.config import TOKEN
from core import logger


class Bot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(command_prefix=".", intents=intents)

    async def setup_hook(self):
        package = "cogs"
        for _, modname, ispkg in pkgutil.walk_packages([package], prefix=package + "."):
            if ispkg:
                continue
            await self.load_extension(modname)
            logger.info(f"Loaded extension: {modname}")

        try:
            synced = await self.tree.sync()
            logger.info(f"Synced {len(synced)} slash commands")
        except Exception as e:
            logger.error(f"Failed to sync commands: {e}")

    async def on_ready(self):
        logger.info(f"Logged in as {self.user}")

    async def on_command_error(self, ctx, error):
        logger.error(f"Command error: {error}")
        traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)

if __name__ == "__main__":
    bot = Bot()
    bot.run(TOKEN)
