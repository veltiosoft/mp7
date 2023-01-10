import asyncio
import logging
import os

import discord
from discord.ext import commands

logging.basicConfig(level=logging.INFO)


intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="$", intents=intents)


async def main():
    async with bot:
        await bot.load_extension("cogs.text_channel")
        await bot.load_extension("cogs.google")
        await bot.load_extension("cogs.thread")

        await bot.start(os.environ["DISCORD_BOT_TOKEN"])


asyncio.run(main())
