import os
from dotenv import load_dotenv
import logging
from enum import Enum
logger = logging.getLogger("discord_bot_logger")

load_dotenv()
def set_env(var_name: str, value: str)-> bool:
    """_summary_
    Setter method for environment varaibles given by the enum class environs
    Args:
        var_name (str): name of the environment variable to set
        value (str): the new value of the environment variable

    Returns:
        bool: true if the environment variable was set with no issues
    """
    try:
        var_name = var_name.name
        os.environ[var_name] = value
        print(f'testing it {os.getenv(var_name, 3000)}')
        return True
    except TypeError as e:
        print(f'Error in the value given: {value}. Error msg: {e}')
        return False       
def get_env(var_name):
    """_summary_

    Args:
        var_name (str): _description_
        default (str): _description_

    Returns:
        str: _description_
    """
    val = var_name.value
    return os.getenv(var_name)
def get_int_env(var_name: str, default: int) -> int:
    """_summary_
    attempt to typecast the environment variable to an integer (it's always returned as string by os.getenv). 
    If successful it will return that, otherwise it will log the error and return the default value
    Args:
        var_name (str): name of the environment variable
        default (int): the default integer value, if the environment variable is not set

    Returns:
        int: the environment variable's value as integer
    """
    try:
        return int(os.getenv(var_name, default))
    except ValueError:
        logger.warning(f"Warning: Environment variable {var_name} is not a valid integer. Using default value {default}.")
        return default

logger.info("Successfully Environsured settings")
    
class Environs(Enum):
        """_summary_
        Create the Environs class to encapsulate the environment variables, import this in the main application using: "from settings import Environs"
        Use Environs.env_var_name to access the environment variable
        """
        #TODO make getting and setting env vars dynamic so no update/re-rerender is needed when changed during runtime
        DEFAULT_TEXT_CHANNEL_NAME = 'DEFAULT_TEXT_CHANNEL_NAME'
        MIN_NUM_USERS = 'MIN_NUM_USERS'
        MAX_NUM_USERS = 'MAX_NUM_USERS'
        DEFAULT_GREETING = 'DEFAULT_GREETING'
        DEFAULT_SLOWMODE_DELAY = 'DEFAULT_SLOWMODE_DELAY'
        LAST_SENT_TIMESTAMP = 'LAST_SENT_TIMESTAMP'
        TOKEN = 'DISCORD_TOKEN'
        command_prefix = 'command_prefix'
        