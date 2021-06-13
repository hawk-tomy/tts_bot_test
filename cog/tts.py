from __future__ import annotations


from logging import getLogger


from discord.ext import commands


logger = getLogger(__name__)


class tts(commands.cog):
    def __init__(self, bot):
        self.bot = bot

        logger.info('load extention is success')

    @commands.command()
    async def join(self, ctx):
        pass


def setup(bot):
    return bot.add_cog(tts(bot))
