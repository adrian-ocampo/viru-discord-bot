from discord.ext import commands
import discord
import datetime
from main import get_prefix
class CommandEvents(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command(self, message):
        CURRENTDATE = datetime.datetime.now().strftime("%Y-%m-%d")
        TIMESTAMP = datetime.datetime.now().strftime("%X")
        channel = message.channel
        channel_id = message.channel.id
        server = message.guild
        command = message.command
        user = message.author
        f = open(f"./logs/{CURRENTDATE}.txt", "a")
        f.write(f"[{TIMESTAMP}] {user}({user.id}) used '{command}' in --> Server: {server.name}({server.id}), Channel: {channel}({channel_id})\n")
        f.close()

    @commands.Cog.listener()
    async def on_command_error(self, message, error):
        prefix = get_prefix(self, message)
        if isinstance(error, commands.CommandNotFound):
            embed=discord.Embed(title=f"Type {prefix}help for a list of commands.", url="", description="", color=0x5AC0FB)
            await message.channel.send(embed=embed) 
        if isinstance(error, commands.MissingAnyRole):
            msg =  f"{message.author.mention}, you do not have permission."
            await message.channel.send(msg)

async def setup(bot):
    await bot.add_cog(CommandEvents(bot)) 

