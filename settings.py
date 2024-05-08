import os
from dotenv import load_dotenv
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("discord_bot_logger")

load_dotenv()
class Config():
    """_summary_
    Create the config class to encapsulate the environment variables, import this in the main application using: "from settings import Config"
    Use Config.env_var_name to access the environment variable
    """
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

    DEFAULT_TEXT_CHANNEL_NAME = os.getenv('DEFAULT_TEXT_CHANNEL_NAME','join_notifications')
    MIN_NUM_USERS = get_int_env('MIN_NUM_USERS', 2)
    MAX_NUM_USERS = get_int_env('MAX_NUM_USERS', 6)
    DEFAULT_GREETING = os.getenv('DEFAULT_GREETING', 'GHOOLS')
    DEFAULT_SLOWMODE_DELAY = get_int_env('DEFAULT_SLOWMODE_DELAY', 300)
    LAST_SENT_TIMESTAMP = get_int_env('LAST_SENT_TIMESTAMP', 0)
    TOKEN = os.getenv('DISCORD_TOKEN', None)
    if not TOKEN:
        logger.error("DISCORD_TOKEN is not set. Please set this environment variable.")
    logger.info("Successfully configured settings")