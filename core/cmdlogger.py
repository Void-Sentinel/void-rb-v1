from core.config import COMMAND_LOG_CHANNEL_ID
import discord


async def send_command_log(ctx):
    channel = ctx.bot.get_channel(COMMAND_LOG_CHANNEL_ID)
    if not isinstance(channel, discord.TextChannel):
        return

    embed = discord.Embed(
        title="Command Executed",
        description=f"> {ctx.author} ran command {ctx.command.name} in channel {ctx.channel.mention}",
        color=discord.Color.red()
    )
    embed.set_thumbnail(url=ctx.author.display_avatar.url)

    await channel.send(embed=embed)
