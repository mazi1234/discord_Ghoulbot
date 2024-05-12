import os
import logging
from dotenv import load_dotenv
load_dotenv()
logger = logging.getLogger("discord_bot_logger")
def getEnvVar(varname: str):
    """_summary_
        Helper method to handle if an env var is present or not
    Args:
        varname (str): name of the environment var is it is stored in memory.

    Returns:
        str: the value of the environment var
    """
    try:
        return os.environ[varname]
    except KeyError as e:
        print(f'Could not find the discord token: {varname}. {e}')
TOKEN = getEnvVar('DISCORD_TOKEN')
logger.info("Successfully configured env vars")