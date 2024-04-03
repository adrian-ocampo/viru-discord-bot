from discord.ext import commands, tasks
import discord
import asyncio
import os
import psutil
import requests
import datetime
import json
from main import get_prefix
class BotCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Commands
    guild_list = [349142555411349514, 371869087355240451]
    ownerID = 153420153789349888
    palworld_command_roles = ["Paldingo", "Palworld", "Pals", "Moderators"]
    palworld_commands = ["run", "close"]
    PROCNAME = "PalServer-Win64-Test-Cmd.exe"
    commandsDescriptions = {
        "cat": "Summon a cat", 
        "dog": "Summon a dog",
        "run": "Opens Palworld Server",
        "close": "Closes Palworld Server",}
    commandsList = list(commandsDescriptions.keys())
    
    @commands.command()
    async def help(self, message):
        prefix = get_prefix(self, message)
        cmdList = ""
        for cmd in self.commandsList:
            if cmd in self.palworld_commands and message.guild.id not in self.guild_list:
                continue
            description = self.commandsDescriptions[cmd]
            cmdList = cmdList + "\n\t**" + cmd + "** : " + description
        embed=discord.Embed(title=f"List of Commands `{prefix}`", description=cmdList, color=0x5AC0FB)
        embed.set_thumbnail(url="{}".format(self.bot.user.avatar.url))
        await message.channel.send(embed=embed) 

    @commands.command()
    async def prefix(self, message, new_prefix):
        with open("prefixes.json", "r") as f:
            prefixes = json.load(f)
        with open("prefixes.json", "w") as f:
            prefixes[str(message.guild.id)] = new_prefix
            json.dump(prefixes, f, indent=4)
        await message.channel.send(f"Prefix changed to `{new_prefix}`")

    @commands.command()
    async def cat(self, message):
        url = 'https://api.thecatapi.com/v1/images/search'
        response = requests.get(url).json()
        await message.channel.send(response[0]["url"])

    @commands.command()
    async def dog(self, message):
        url = 'https://dog.ceo/api/breeds/image/random'
        response = requests.get(url).json()
        await message.channel.send(response["message"])


    @commands.command(aliases=["open", "start"])
    @commands.has_any_role(*palworld_command_roles)
    async def run(self, message):
        if message.guild.id not in self.guild_list:
            await message.channel.send("Sorry! Command not available in this server.")
            return
        msg = "Server is now open."
        if not self.bot.runningServer:
            os.startfile("D:\\SteamLibrary\\steamapps\\common\\PalServer\\PalworldServer.bat")
            self.backupServer.start()
            self.bot.runningServer = True
        else:
            msg = "Server already running!"
        await message.channel.send(msg)

    @commands.command()
    @commands.has_any_role(*palworld_command_roles)
    async def close(self, message):
        if message.guild.id not in self.guild_list:
            await message.channel.send("Sorry! Command not available in this server.")
            return
        msg = ""
        if self.bot.runningServer:
            await message.channel.send("Server is closing.")
            os.startfile("D:\\SteamLibrary\\steamapps\\common\\PalServer\\Backup.bat")
            await asyncio.sleep(3)
            for proc in psutil.process_iter():
                # check whether the process name matches
                if proc.name() == self.PROCNAME:
                    proc.kill()
                    self.bot.runningServer = False
                    self.backupServer.stop()
            msg = "Server closed!"
        else:
            msg = "Server is not up!"
        await message.channel.send(msg)

    # Tasks
    @tasks.loop(hours=1) 
    async def backupServer():
        os.startfile("D:\\SteamLibrary\\steamapps\\common\\PalServer\\Backup.bat")
        print("Backup created on: " + str(datetime.datetime.now()))

async def setup(bot):
    await bot.add_cog(BotCommands(bot)) 

