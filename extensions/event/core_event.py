import discord
from discord.ext import commands
from core.classes import Cog_Extension
from yaml import load
from pathlib import Path
import os
import random
import re
try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader

with open("discord_config.yaml", encoding='utf-8') as f:
    config = load(f, Loader=Loader)


class CoreEvent(Cog_Extension):
    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = self.bot.get_channel(config['main_channel'])
        to_send = f'Welcome {member}!'
        await channel.send(to_send)

    @commands.Cog.listener()
    async def on_member_leave(self, member):
        channel = self.bot.get_channel()
        to_send = f'{member} is leave!'
        await channel.send(to_send)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return
        # we do not want the bot to reply to itself
        print(message.content)
        special = config['special']
        special_should_key = special['should'].keys()
        # 關鍵字處理
        for key in special_should_key:
            if key in message.content:
                dir_path = os.path.join(Path().absolute(),
                                        'src',
                                        special[key])
                file_list = []
                for root, dirs, files in os.walk(dir_path):
                    for file in files:
                        file_list.append(os.path.join(root, file))
                print(file_list)
                choice_file = random.choice(file_list)
                if choice_file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.webp')):
                    pic = discord.File(choice_file)
                    await message.channel.send(file=pic)
                else:
                    with open(choice_file, encoding='utf-8') as f:
                        text = f.read()
                    await message.channel.send(text)

        if "機率" in message.content:
            await message.channel.send(f'{random.random()*100:0.02f} %')
        # # nhentai 處理
        # if 'nhentai' in message.content:
        #     num_list = re.findall(r'(?!\d\/)\d+', message.content)
        #     for num in num_list:
        #         await message.channel.send(f"https://nhentai.net/g/{num}/")
        # if 'pixiv' in message.content:
        #     num_list = re.findall(r'(?!\d\/)\d+', message.contemt)
        #     for num in num_list:
        #         await message.channel.send(f"https://www.pixiv.net/artworks/{num}")
        return

def setup(bot):
    bot.add_cog(CoreEvent(bot))
