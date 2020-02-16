import discord
from discord.ext import commands
from core.classes import Cog_Extension


class Repeat(Cog_Extension):
    @commands.command()
    async def repeat(self, ctx, *message):
        await ctx.message.delete()
        await ctx.send(' '.join(message))


def setup(bot):
    bot.add_cog(Repeat(bot))
