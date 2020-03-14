import asyncio
import logging

import discord
from discord.ext import commands, tasks

import config

class Bot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.case_insensitive = True

        self.logger = logging.getLogger('discord')
        self.logger.setLevel(logging.INFO)
        self.handler = logging.FileHandler(
            filename='bot.log', encoding='utf-8', mode='w')
        self.handler.setFormatter(
            logging.Formatter(
                '%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
        self.logger.addHandler(self.handler)
        
        self.BOT_NAME = config.BOT_NAME
        self.EMBED_COLOR = config.EMBED_COLOR
        self.TOKEN = config.DISCORD_TOKEN
        self.PREFIX = config.DISCORD_PREFIX
        self.API_KEY = config.API_KEY
        self.ADMINS = config.ADMINS

        extensions = ["cogs.stats",
                      "cogs.admin",
                      "cogs.help"
                    ]
        
        for e in extensions:
            self.load_extension(e)

    async def on_ready(self):
        print("Bot Started.")
        change_status.start()

client = Bot(commands.when_mentioned_or(config.DISCORD_PREFIX))

@tasks.loop(seconds=10)
async def change_status():
    try:
        await client.change_presence(
            activity=discord.Activity(
                name=f'{len(client.users)} Users - {len(client.guilds)} Guilds',
                type=discord.ActivityType.watching))
        await asyncio.sleep(10)
        await client.change_presence(
            activity=discord.Game(name=f"Use my prefix {client.PREFIX} or @me!"))
    except Exception as error:
        print(error)

client.run(client.TOKEN)
