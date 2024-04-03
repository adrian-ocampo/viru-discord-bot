from discord.ext import commands
import discord
import psutil
import json
from main import get_prefix
class BotEvents(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    PROCNAME = "PalServer-Win64-Test-Cmd.exe"

    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.playing, name="Palworld"))
        for proc in psutil.process_iter():
            # check whether the process name matches
            if proc.name() == self.PROCNAME:
                self.bot.runningServer = True
            else:
                self.bot.runningServer = False
        print(f"{self.bot.user} is up and running.")

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        with open('prefixes.json', 'r') as f:
            prefixes = json.load(f)
        prefixes[str(guild.id)] = '!!'
        with open('prefixes.json', 'w') as f:
            json.dump(prefixes, f, indent=4)

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        with open('prefixes.json', 'r') as f:
            prefixes = json.load(f)
        prefixes.pop(str(guild.id))
        with open('prefixes.json', 'w') as f:
            json.dump(prefixes, f, indent=4)

    @commands.Cog.listener()
    async def on_message(self, message):
        # Responses

        if message.author == self.bot.user:
            return
        
        if self.bot.user.mentioned_in(message):
            await message.channel.send(f"Server Prefix is `{get_prefix(self, message)}`")

        #if message.content.lower().startswith("hello"):
            #await message.channel.send("Hello!")
        #await self.bot.process_commands(message)

async def setup(bot):
    await bot.add_cog(BotEvents(bot)) 

