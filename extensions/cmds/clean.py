import discord
from discord.ext import commands
from core.classes import Cog_Extension
import datetime


class Clean(Cog_Extension):
    @commands.command()
    async def clean(self, ctx, cnt: int = 0):
        await ctx.channel.purge(limit=cnt+1, before=datetime.datetime.now())


def setup(bot):
    bot.add_cog(Clean(bot))
