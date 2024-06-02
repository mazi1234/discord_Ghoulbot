import discord
from discord.ext import commands
from config import cmdConfig as config, cmdList as cmds, SettingConfig as envConfig
from env_vars import TOKEN
import logging
logger = logging.getLogger("discord_bot_logger")
intents = discord.Intents.all()
cmd_prefix = config.get("command_prefix", "!")
bot = commands.Bot(command_prefix=cmd_prefix, intents=intents, 
                   help_command=commands.MinimalHelpCommand())
@bot.group(invoke_without_command=True)
async def show(ctx):
    await ctx.send('command {ctx} not found')
#-------------------------------------------------------------------------------------------------------
@bot.group(invoke_without_command=True)
async def set(ctx):
    """_summary_
    Handles any set commands that are not explicitly handled in their own functions
    Args:
        ctx (discord.ext.commands.Context): The context this command was called under
    """
    await ctx.send('command {ctx} not found')
@set.command(name=cmds.get("set_min_users"))
async def set_min_users(ctx, arg:int =None):
    """_summary_
    Sets the minimum number of users that must join before a notification is sent
    Args:
        ctx (discord.ext.commands.Context): The context this command was called under
        arg (int, optional): The new value for the minimum number of users . Defaults to None.
    """
    if (await isValidArg(ctx, arg)):
        old = cmds.get("set_min_users")
        envConfig.set(cmds.get("set_min_users"), arg)
        logger.info(f'Successfully configured the {cmds.get("set_min_users")} to {arg} from {old}')
@set.command(name=cmds.get("set_max_users"))
async def set_max_users(ctx, arg:int=None):
    """_summary_
        Changes the maximum number of users the bot will send join notifications for. After the maximum users have joined, the bot will not send any more notifications to the text channel
    Args:
        ctx (discord.ext.commands.Context): The context this command was called under
        arg (int, optional): The new value for the maximum number of users. Defaults to None.
    """
    if (await isValidArg(ctx,arg)):
        old = cmds.get("set_max_users")
        envConfig.set(cmds.get("set_max_users"), arg)
        logger.info(f'Successfully configured the {cmds.get("set_max_users")} to {arg} from {old}')
@bot.event
async def on_ready():
    """_summary_
    Runs when the client is connected and recieves a ready signal from discord
    Returns:
        None
    """
    print(f'{bot.user} has connected to Discord!')
    print(bot.guilds)
async def isValidArg(ctx, arg) -> bool:
    """_summary_
    Checks if the argument is valid or missing. If missing it will alert the user in discord (by sending a message) and also logging the failure.
    Args:
        ctx (discord.ext.commands.Context): the context of the command.
        arg (any): the argument to check if missing or not

    Returns:
        bool: True if the argument is valid. False if missing
    """
    if arg is None: 
        await ctx.send(f'Invalid Command. Error: Missing argument. Use {cmd_prefix}help to print the manual')
        logger.info(f'There\'s a missing argument. Context {ctx}')
        return False
    return True
bot.run(TOKEN)
