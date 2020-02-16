import discord
from discord.ext import commands
from core.classes import Cog_Extension
import re
import aiohttp
import json
import datetime
import base64


class nHentai(Cog_Extension):
    @commands.command()
    async def n(self, ctx, *messages):

        await ctx.channel.purge(limit=1, before=datetime.datetime.now())
        for message in messages:
            num_list = re.findall(r'(?!\d\/)\d+', message)
            for num in num_list:
                async with aiohttp.request('GET', f'https://nhentai.net/api/gallery/{num}') as resp:
                    if 200 <= resp.status < 300:
                        r = await resp.json()
                        tags = {}
                        embed = discord.Embed(title=r['title']['english'],
                                              url=f'https://nhentai.net/g/{num}/',
                                              description=r['title']['japanese'],
                                              color=0xeb14c0,
                                              timestamp=datetime.datetime.utcnow())
                        embed.set_author(name="nHentai")
                        embed.set_thumbnail(url=f'https://t.nhentai.net/galleries/{r["media_id"]}/cover.jpg')
                        for i in r['tags']:
                            if i['type'] in tags:
                                tags[i['type']].append(i['name'].capitalize())
                            else:
                                tags[i['type']] = [i['name'].capitalize()]
                        for key in tags.keys():
                            embed.add_field(name=key.capitalize(), value=", ".join(tags[key]), inline=True)
                        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(nHentai(bot))
