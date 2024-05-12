from env_vars import getEnvVar
import logging
import json
logger = logging.getLogger("discord_bot_logger")
class Config:
    def __init__(self, filename):
        """_summary_
        initializes the class by loading the json file given by filename
        Args:
            filename (_type_): _description_
        """
        self.filename = filename
        try:
            with open(filename, 'r') as file:
                self.config_data = json.load(file)
        except Exception as e:
            print(f'Error occured while initializing config file: {e}')
    def get(self, key, default=None):
        """_summary_

        Args:
            key (_type_): _description_
            default (_type_, optional): _description_. Defaults to None.

        Returns:
            _type_: _description_
        """
        return self.config_data.get(key, default)
    def set(self, key, value):
        """_summary_
        Setter method to adjust the value of a var in the settings json file
        Args:
            key (_type_): _description_
            value (_type_): _description_
        """
        self.config_data[key] = value
        self.save()
    def save(self):
        """_summary_
        """
        try:
            with open(self.filename, 'w') as file:
                json.dump(self.config_data, file, indent=4)
        except Exception as e:
            print(f'Error occured while saving config file: {e}')
    def as_dict(self)->dict:
        """_summary_

        Returns:
            dict: _description_
        """
        return self.config_data

configFile: str = getEnvVar('config_file')
SettingConfig = Config(configFile)
configDict = SettingConfig.as_dict()

commandsFile: str = getEnvVar('commands_file')
cmdConfig = Config(commandsFile)
cmdList = cmdConfig.as_dict()
logger.info("Successfully configured Config")