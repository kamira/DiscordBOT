import discord
from discord.ext import commands
from core.classes import Cog_Extension
import datetime
import asyncio


class Task(Cog_Extension):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.channel = None
        self.unsend = True
        self.bg_task = None


    @commands.command()
    async def time_task(self, ctx, *message):
        cmd = message[0]
        print(message)
        if cmd == "set":
            channel_id = int(message[1])
            self.channel = self.bot.get_channel(channel_id)
            await ctx.send(f'Set Channel: {self.channel.mention}')

        if cmd == "start":
            if self.channel is None:
                await ctx.send('Please set channel first')
            else:
                self.bg_task = self.bot.loop.create_task(self.task_time())
                await ctx.send('Start Task Succeed')

        if cmd == "end":
            if self.bg_task is not None:
                self.bg_task.cancel()
                self.bg_task = None
            else:
                await ctx.send("Time task is not set.")

    async def task_time(self):
        await self.bot.wait_until_ready()
        while not self.bot.is_closed():
            date = datetime.datetime.now()
            if date.second == 0 and date.minute == 0:
                if self.unsend:
                    await self.channel.send(date.strftime("%Y/%m/%d %H:%M:%S"))
                    self.unsend = False
            else:
                self.unsend = True
            await asyncio.sleep(0.1)


def setup(bot):
    bot.add_cog(Task(bot))
