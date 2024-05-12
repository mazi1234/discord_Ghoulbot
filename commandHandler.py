import discord
from config import MyConfig, cmdList
from discord.ext import commands
from env_vars import TOKEN
intents = discord.Intents.all()
cmd_prefix = MyConfig.get("command_prefix", "!")
bot = commands.Bot(command_prefix=cmd_prefix, intents=intents)
#set_ varname val
@bot.command
def commandHandler(cmdList):
    print(type(cmdList))
    for key, val in cmdList:
        if key.startswith("set"):
            print("setter")
            configVarName = val
            MyConfig.set(configVarName, )

@bot.command(name=cmdList.get("set_min_users"))
async def change_min_users(ctx, arg=None):
    handleMissingArg(ctx, arg)
    config.set_env()
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
bot.run(TOKEN)
