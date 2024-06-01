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

    Args:
        ctx (_type_): _description_
    """
    await ctx.send('command {ctx} not found')
@set.command(name=cmds.get("set_min_users"))
async def set_min_users(ctx, arg=None):
    """_summary_

    Args:
        ctx (_type_): _description_
        arg (_type_, optional): _description_. Defaults to None.
    """
    if (await handleMissingArg(ctx, arg)):
        old = cmds.get("set_min_users")
        envConfig.set(cmds.get("set_min_users"), arg)
        logger.info(f'Successfully configured the {cmds.get("set_min_users")} to {arg} from {old}')
@set.command(name=cmds.get("set_max_users"))
async def set_max_users(ctx, arg=None):
    """_summary_
        Changes the maximum number of users the bot will send join notifications for. After the maximum users have joined, the bot will not send any more notifications to the text channel
    Args:
        ctx (_type_): _description_
        arg (_type_, optional): _description_. Defaults to None.
    """
    if (await handleMissingArg(ctx,arg)):
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
async def handleMissingArg(ctx, arg) -> bool:
    if arg == None: 
        await ctx.send(f'Invalid Command. Error: Missing argument. Use {cmd_prefix}help to print the manual')
        return False
    return True
bot.run(TOKEN)
