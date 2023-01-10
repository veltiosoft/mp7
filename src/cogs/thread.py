import datetime
import json
import logging
from dataclasses import asdict, dataclass

import aiofiles
import discord
from aiofiles.os import remove
from discord.ext import commands

logger = logging.getLogger(__name__)


@dataclass
class ValidResult:
    ok: bool
    message: str


@dataclass
class ExportMessage:
    message_id: int
    author_id: int
    author_name: str
    content: str
    created_at: str


class ManageThread(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    async def export_thread(self, ctx: commands.Context):
        logger.info(ctx.message)
        valid_res = self.valid(ctx)
        if not valid_res.ok:
            await ctx.send(f"{valid_res.message}")
            return

        ch: discord.Thread = ctx.channel
        logger.info(f"約 {ch.message_count} 件のメッセージがあります")
        await ctx.send(f"約 {ch.message_count} 件のメッセージがあります")

        # TODO: メッセージの形式を csv とか選べるようにする
        try:
            file_name = f"{ch.name}_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}.json"
            async with aiofiles.open(file_name, encoding="utf-8", mode="w") as f:
                res = []
                async for msg in ch.history(oldest_first=True):
                    res.append(
                        asdict(ExportMessage(msg.id, msg.author.id, msg.author.name, msg.content, msg.created_at.isoformat()))
                    )

                await f.write(json.dumps(res, indent=2, ensure_ascii=False))

            await ctx.send("エクスポートが完了しました", file=discord.File(fp=file_name))
            # 完了したらファイルを削除する
            await remove(file_name)
        except discord.Forbidden as e:
            msg = "メッセージ履歴を読み取る権限がありません!"
            logger.error(msg, exc_info=True)
            await ctx.send(msg)
            raise e
        except discord.HTTPException as e:
            msg = "メッセージ履歴の取得に失敗しました!"
            logger.error(msg, exc_info=True)
            await ctx.send(msg)
            raise e

    def valid(self, ctx: commands.Context) -> ValidResult:
        ch = ctx.channel

        if ch.type != discord.ChannelType.public_thread:
            return ValidResult(False, "public thread でのみ実行できるコマンドです")

        return ValidResult(True, "")


async def setup(bot: commands.Bot):
    await bot.add_cog(ManageThread(bot))
