import discord
import re
from pathlib import Path
from discord.ext import commands
from discord.ext.commands import command
from yaml import load, dump
from event import bot_event
import os
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

with open("discord_config.yaml", encoding='utf-8') as f:
    config = load(f, Loader=Loader)

bot = commands.Bot(command_prefix='!')

extension_list = []

@bot.event
async def on_ready():
    print(">> BOT ONLINE <<")
    print('-' * 20)


@bot.command()
async def load(ctx, *extensions):
    for ext in extensions:
        print(ext)
    [bot.load_extension(f'extensions.{extension}') for extension in extensions]
    await ctx.send(f'Loaded: {", ".join(extensions)}')


@bot.command()
async def unload(ctx, *extensions):
    for ext in extensions:
        print(ext)
    [bot.unload_extension(f'extensions.{extension}') for extension in extensions]
    await ctx.send(f'Un-Loaded: {", ".join(extensions)}')


@bot.command()
async def reload(ctx, *extensions):
    for ext in extensions:
        print(ext)
    [bot.reload_extension(f'extensions.{extension}') for extension in extensions]
    await ctx.send(f'Re-Loaded: {", ".join(extensions)}')


# bot_event(bot, config)


dir_path = os.path.join(Path().absolute(), 'extensions')
for root, dirs, files in os.walk(dir_path):
    for file in files:
        if file.endswith('.py'):
            extension = str(root).replace(str(Path().absolute()), "").split("\\")[1:]
            bot.load_extension(f'{".".join(extension)}.{file[:-3]}')


def main():
    bot.run(config['token'])


if __name__ == "__main__":
    main()