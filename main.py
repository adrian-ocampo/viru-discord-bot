import discord
import asyncio
import nest_asyncio
from key import TOKEN
from discord.ext import commands
import os
import json
nest_asyncio.apply()
intents = discord.Intents.default()
intents.members = True
intents.message_content = True

def get_prefix(bot, message):
    with open("prefixes.json", "r") as f:
        prefix = json.load(f)
        return prefix[str(message.guild.id)]
bot = commands.Bot(command_prefix=get_prefix, intents=intents)
prefix = bot.command_prefix
bot.remove_command('help')

async def load_extensions():
    for filename in os.listdir("cogs"):
        if filename.endswith(".py"):
            await bot.load_extension(f"cogs.{filename[:-3]}")
        
async def main():
    await load_extensions()
    await bot.start(TOKEN)

asyncio.run(main()) 