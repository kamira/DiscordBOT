import discord
from discord.ext import commands
from core.classes import Cog_Extension
import re
import aiohttp
import datetime
import base64
from io import BytesIO


header = {
    "referer": "https://www.pixiv.net/"
}



class Pixiv(Cog_Extension):
    @commands.command()
    async def p(self, ctx, *messages):

        # await ctx.channel.purge(limit=1, before=datetime.datetime.now())
        async def img_url(url):
            file = None
            async with aiohttp.request('GET', url, headers=header) as r:
                if 200 <= r.status < 300:
                    datatype = r.headers['Content-Type'].split('/')[1]
                    with BytesIO(await r.read()) as output:
                        file = discord.File(output, filename=f'thumbnail.{datatype}')
            return file

        for message in messages:
            num_list = re.findall(r'(?!\d\/)\d+', message)
            for num in num_list:
                async with aiohttp.request('GET', f'https://www.pixiv.net/ajax/illust/{num}', headers=header) as resp:
                    print(resp.status)
                    if 200 <= resp.status < 300:
                        r = await resp.json()
                        # 圖片資訊
                        embed = discord.Embed(title=r['body']['illustTitle'],
                                              url=f'https://www.pixiv.net/artworks/{num}/',
                                              description=r['body']['description'].replace('<br />', '\n'),
                                              color=0xff8000,
                                              timestamp=datetime.datetime.utcnow())

                        print('set_thumbnail')
                        # 作者資訊
                        async with aiohttp.request('GET', f'https://www.pixiv.net/ajax/user/{r["body"]["userId"]}?full=0', headers=header) as author_resp:
                            if 200 <= author_resp.status < 300:
                                author_r = await author_resp.json()

                                embed.set_author(name=author_r['body']['name'],
                                                 url=f'https://www.pixiv.net/users/{r["body"]["userId"]}')
                                print(author_r['body']['imageBig'])
                        tags = [tag['tag'] for tag in r['body']['tags']['tags']]
                        embed.add_field(name="Tags", value=", ".join(tags), inline=True)
                        file = await img_url(r["body"]['urls']['small'])
                        await ctx.send(file=file, embed=embed)
                    else:
                        print(await resp.content.read())


def setup(bot):
    bot.add_cog(Pixiv(bot))
