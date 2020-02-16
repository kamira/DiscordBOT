import discord
from discord.ext import commands
from core.classes import Cog_Extension
import re
import aiohttp
import json
import datetime


class eHentai(Cog_Extension):
    @commands.command()
    async def e(self, ctx, *messages):
        await ctx.channel.purge(limit=1, before=datetime.datetime.now())

        async def ehentai_detail(_id, token):
            async with aiohttp.request(
                    'POST',
                    f'https://api.e-hentai.org/api.php',
                    json={
                        "method": "gdata",
                        "gidlist": [[int(_id), token]],
                        "namespace": 1
                    }) as resp:
                if 200 <= resp.status < 300:
                    r = json.loads(await resp.content.read())
                    print(json.dumps(r, indent=4))
                    embed = discord.Embed(title=r['gmetadata'][0]['title'],
                                          url=f'https://e-hentai.org/g/{_id}/{token}',
                                          description=r['gmetadata'][0]['title_jpn'],
                                          color=0xc90724,
                                          timestamp=datetime.datetime.utcnow())
                    embed.set_author(name=r['gmetadata'][0]["category"])
                    embed.set_thumbnail(url=r['gmetadata'][0]['thumb'])
                    # Rating
                    embed.add_field(name="Rating", value=r['gmetadata'][0]['rating'], inline=True)
                    tags = {}
                    for i in r['gmetadata'][0]['tags']:
                        k_v = i.split(":")
                        if len(k_v) == 1:
                            k_v = ["Misc", k_v[0]]
                        if k_v[0] in tags:
                            tags[k_v[0]].append(k_v[1])
                        else:
                            tags[k_v[0]] = [k_v[1]]
                    for key in tags.keys():
                        embed.add_field(name=key.capitalize(), value=", ".join(tags[key]), inline=True)
                    await ctx.send(embed=embed)

        async def page_detail(_id: str, p_token: str, p_num: str):
            async with aiohttp.request(
                    'POST',
                    f'https://api.e-hentai.org/api.php',
                    json={
                        "method": "gtoken",
                        "pagelist": [[int(_id), p_token, int(p_num)]]
                    }) as resp:
                if 200 <= resp.status < 300:
                    r = json.loads(await resp.content.read())
                    print(json.dumps(r, indent=4))
                    return r["tokenlist"][0]['gid'], r["tokenlist"][0]['token']
                return None, None

        for message in messages:
            if re.match(r"[\w:\/\-\.]+g\/\d+\/\w+", message):
                m = re.search(r"g\/(?P<id>\d+)\/(?P<token>\w+)", message)
                await ehentai_detail(m.group("id"), m.group("token"))
            elif re.match(r"[\w:\/\-\.]+s\/\w+\/\d+\-", message):
                m = re.search(r"s\/(?P<p_token>\w+)\/(?P<id>\d+)\-(?P<p_num>\d+)", message)
                (b_id, token) = await page_detail(m.group("id"), m.group("p_token"), m.group("p_num"))
                print((b_id, token))
                if b_id is not None:
                    await ehentai_detail(b_id, token)





def setup(bot):
    bot.add_cog(eHentai(bot))
