import traceback
import discord
from discord.ext import commands
from config import cmdConfig as config, cmdList as cmds, SettingConfig as envConfig
from traceback import format_exc
import logging
# @bot.group(name="show",invoke_without_command=False)
# async def show(ctx):
#     await ctx.send(f'command not found')
# @show.command(name="show_all")
# async def show_all(ctx, arg=None):
#     await ctx.send(f'{arg}')
#-------------------------------------------------------------------------------------------------------
class myCmds(commands.Cog):
    def __init__(self, bot, logger):
        self.bot = bot
        self.logger = logger
    @commands.group(invoke_without_command=True)
    async def set(self, ctx):
        """_summary_
        Handles any set commands that are not explicitly handled in their own functions
        Args:
            ctx (discord.ext.commands.Context): The context this command was called under
        """
        await ctx.send(f'command not found')
    @set.command(name=cmds.get("set_min_users"))
    async def set_min_users(self, ctx, arg:int =None):
        """_summary_
        Sets the minimum number of users that must join before a notification is sent
        Args:
            ctx (discord.ext.commands.Context): The context this command was called under
            arg (int, optional): The new value for the minimum number of users . Defaults to None.
        """
        if (await self.isValidArg(ctx, arg)):
            old = cmds.get("set_min_users")
            envConfig.set(cmds.get("set_min_users"), arg)
            self.logger.info(f'Successfully configured the {cmds.get("set_min_users")} to {arg} from {old}')
    @set.command(name=cmds.get("set_max_users"))
    async def set_max_users(self, ctx, arg:int=None):
        """_summary_
            Changes the maximum number of users the bot will send join notifications for. After the maximum users have joined, the bot will not send any more notifications to the text channel
        Args:
            ctx (discord.ext.commands.Context): The context this command was called under
            arg (int, optional): The new value for the maximum number of users. Defaults to None.
        """
        if (await self.isValidArg(ctx,arg)):
            old = cmds.get("set_max_users")
            envConfig.set(cmds.get("set_max_users"), arg)
            self.logger.info(f'Successfully configured the {cmds.get("set_max_users")} to {arg} from {old}')
    @set.command(name=cmds.get("set_command_prefix"))
    async def set_command_prefix(self, ctx, arg:str=None):
        if (await self.isValidArg(ctx, arg)):
            old = cmds.get("set_command_prefix")
            envConfig.set(cmds.get("set_command_prefix"), arg)
            self.logger.info(f'Successfully configured the {cmds.get("set_command_prefix")} to {arg} from {old}')
    @set.command(name=cmds.get("set_greeting"))
    async def set_greeting(self, ctx, arg:str=None):
        if (await self.isValidArg(ctx, arg)):
            old = cmds.get("set_greeting")
            envConfig.set(cmds.get("set_greeting"), arg)
            self.logger.info(f'Successfully configured the {cmds.get("set_greeting")} to {arg} from {old}')
    @set.command(name=cmds.get("set_slowmode_delay"))
    async def set_slowmode_delay(self, ctx, arg:int=None):
        if (await self.isValidArg(ctx, arg)):
            old = cmds.get("set_slowmode_delay")
            envConfig.set(cmds.get("set_slowmode_delay"), arg)
            self.logger.info(f'Successfully configured the {cmds.get("set_slowmode_delay")} to {arg} from {old}')
    @set.command(name=cmds.get("set_text_channel_name"))
    async def set_text_channel_name(self, ctx, arg:str=None):
        if (await self.isValidArg(ctx, arg)):
            old = cmds.get("set_text_channel_name")
            envConfig.set(cmds.get("set_text_channel_name"), arg)
            self.logger.info(f'Successfully configured the {cmds.get("set_text_channel_name")} to {arg} from {old}')
    @set_min_users.error
    async def on_application_command_error(self, ctx, error: discord.DiscordException):
        await ctx.send(f'An error occurred. Sending traceback {ctx.args} {error}')
        self.logger.Error(f'An error occurred. Sending traceback {ctx.args} {error}')
        full_error = traceback.format_exception(error)
        await ctx.channel.send(f"**An exception has occurred!** (User {ctx.me} used /"
                    f"{ctx.command.qualified_name} with args {ctx.selected_options})\n```py\n{''.join(full_error)}```")
    
    async def isValidArg(self, ctx, arg) -> bool:
        """_summary_
        Checks if the argument is valid or missing. If missing it will alert the user in discord (by sending a message) and also logging the failure.
        Args:
            ctx (discord.ext.commands.Context): the context of the command.
            arg (any): the argument to check if missing or not

        Returns:
            bool: True if the argument is valid. False if missing
        """
        if arg is None: 
            await ctx.send(f'Invalid Command. Error: Missing argument. Use {cmds.get("command_prefix")}help to print the manual')
            self.logger.warning(f'There\'s a missing argument. Context {ctx}')
            return False
        return True
