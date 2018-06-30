import discord
from discord.ext import commands
import json
import os
import asyncio
import lavalink
from datetime import datetime


class WeirdnessBot(commands.AutoShardedBot):

    def __init__(self):
        self._prefix = '$'
        super().__init__(command_prefix=self._prefix)
        self.remove_command('help')

        self.config = json.loads(open('config.json', 'r').read())
        self.music_client = lavalink.Client(bot=self, password=self.config['lavalinkpass'], loop=self.loop, ws_port=1337)
        self.launch_time = datetime.utcnow()
        self.bg_task = self.loop.create_task(self.status_task())

        for file in os.listdir("modules"):
            if file.endswith(".py"):
                name = file[:-3]
                try:
                    self.load_extension(f"modules.{name}")
                except Exception:
                    print(f"The {name} module failed to load. Please repair it and load it.")

    async def on_ready(self):
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)

    async def on_message(self, message):
        if message.author == self.user:
            return
        if message.content == "HAIL HYDRA!":
            await message.channel.send("***HAIL HYDRA!!!***")
        await self.process_commands(message)

    async def on_command_error(self, context, exception):
        if isinstance(exception, discord.ext.commands.errors.MissingRequiredArgument):
            await context.send("You're missing one or more required arguments.")
        elif isinstance(exception, discord.ext.commands.errors.BotMissingPermissions):
            await context.send("I am missing the required permissions to perform this command successfully.")
        elif isinstance(exception, discord.ext.commands.errors.MissingPermissions):
            await context.send("You do not have permission to perform this command.")
        elif isinstance(exception, discord.ext.commands.errors.CommandNotFound):
            pass
        else:
            await context.send("An error has occurred.")

    async def status_task(self):
        while not self.is_closed():
            await self.change_presence(activity=discord.Activity(name='Do \"$help\" for help', type=discord.ActivityType.playing))
            await asyncio.sleep(300)
            await self.change_presence(activity=discord.Activity(name='$help | PyCharm Community', type=discord.ActivityType.playing))
            await asyncio.sleep(300)
            await self.change_presence(activity=discord.Activity(name='$help | 24K Magic', type=discord.ActivityType.listening))
            await asyncio.sleep(300)
            await self.change_presence(activity=discord.Streaming(name='$help | Doctor Who', url="https://twitch.tv/TwitchPresents"))
            await asyncio.sleep(300)

    async def restart_music(self):
        del self.music_client
        self.music_client = lavalink.Client(bot=self, password=self.config['lavalinkpass'], loop=self.loop,
                                            ws_port=1337)


client = WeirdnessBot()
config = json.loads(open('config.json', 'r').read())
client.run(config.get('discordtoken'))