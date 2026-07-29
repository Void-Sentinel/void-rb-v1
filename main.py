import discord
from discord.ext import commands
import traceback
import sys
import pkgutil
from core.config import TOKEN
from core.cmdlogger import send_command_log


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
            print(f"Loaded extension: {modname}")

        try:
            synced = await self.tree.sync()
            print(f"Synced {len(synced)} slash commands")
        except Exception as e:
            print(f"Failed to sync commands: {e}")

    async def on_ready(self):
        print(f"Logged in as {self.user}")

    async def on_command(self, ctx):
        await send_command_log(ctx)

    async def on_command_error(self, ctx, error):
        traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)

    @commands.command(name="sync")
    @commands.is_owner()
    async def sync(self, ctx):
        synced = await self.tree.sync()
        await ctx.send(f"Synced {len(synced)} slash commands")


if __name__ == "__main__":
    bot = Bot()
    bot.run(TOKEN)
