import discord
import asyncio
from utils import config as cfg
from typing import *


class EmbedFactory:
    @staticmethod
    async def prompt(ctx, bot, desc: str, body: str = None, *, check, timeout: int = 60, delete: bool = False) -> Optional[str]:
        embed = discord.Embed(
            description=desc,
            colour=cfg.colors.WSU_GOLD
        )
        if body is not None:
            prompt = await ctx.send(body, embed=embed)
        else:
            prompt = await ctx.send(embed=embed)

        try:
            response = await bot.wait_for('message', check=check, timeout=60)
        except asyncio.TimeoutError:
            await ctx.send(embed=discord.Embed(
                description="Took too long to respond!",
                colour=cfg.colors.TIMEOUT
            ))
            return

        ans = response.content

        if delete:
            await prompt.delete()
            await response.delete()

        return ans

    @staticmethod
    async def success(ctx, desc: str):
        await ctx.send(embed=discord.Embed(
            description=desc,
            colour=cfg.colors.SUCCESS
        ))

    @staticmethod
    async def error(ctx, desc: str):
        await ctx.send(embed=discord.Embed(
            description=desc,
            colour=cfg.colors.ERROR
        ))
