import discord
from settings import get_env, set_env, get_int_env
from settings import Environs
from dotenv import load_dotenv
from discord.ext import commands
from enum import Enum
load_dotenv()
intents = discord.Intents.all()
bot = commands.Bot(command_prefix=get_env(Environs.command_prefix), intents=intents)
class Commands(Enum):
    set_min_users = 'set_min_users'
    set_max_users = 'set_max_users'
    set_greeting = 'set_greeting'
    set_slowmode_delay = 'set_slowmode_delay'
    manual_cmd = 'man'
    help_cmd = 'help'
    set_command_prefix = 'set_command_prefix'
    set_text_channel_name = 'set_text_channel_name'
@bot.command(name=Commands.set_min_users)
async def change_min_users(ctx, arg=None):
    handleMissingArg(ctx, arg)
    assert(isinstance(arg, str))
    print(f' first {get_env(Environs.MIN_NUM_USERS)}')
    set_env(Environs.MIN_NUM_USERS, arg)
    print(f'LAST {get_env(Environs.MIN_NUM_USERS)}')
@bot.event
async def on_ready():
    """_summary_
    Runs when the client is connected and recieves a ready signal from discord
    Returns:
        None
    """
    print(f'{bot.user} has connected to Discord!')
    print(bot.guilds)
async def handleMissingArg(ctx, arg):
    if arg == None: 
        return await ctx.send(f'Missing argument. Use {Environs.command_prefix}{Commands.set_min_users} to print the manual to')
bot.run(get_env(Environs.TOKEN))
