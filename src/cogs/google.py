import logging
from urllib.parse import quote_plus

from discord.ext import commands

from views.button import LinkButton

logger = logging.getLogger(__name__)


class Google(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    async def google(self, ctx: commands.Context, *, query: str):
        logger.info(ctx.args)
        url = f"https://www.google.com/search?q={quote_plus(query)}"
        await ctx.send(view=LinkButton("Go to top on this channe", url))


async def setup(bot: commands.Bot):
    await bot.add_cog(Google(bot))
