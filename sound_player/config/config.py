import configparser
import os
import json
#from ..entity.sound_option import SoundOption
from ..entity.sound_set import SoundSet


class Config:
    """
    Class that manages operating environment information

    Attributes:
        home_path :  Your system's home directory
        config  : Object of class configparser
    """

    def __init__(self):
        self.home_path = os.path.expanduser("~")

        self.config = configparser.ConfigParser()
        self.config.read(self.home_path + "/RobotData/sound/config/config.ini")

        option_path = self.home_path + self.config["CONFIG"].get("option_path")
        option_file = self.config["CONFIG"].get("option_file")

        data = self._load_option_file(option_path, option_file)

        soundSet = SoundSet(**data)            
        self.sound_list = soundSet.sound                     

        self.code_list = dict(map(lambda obj: (obj.code, obj), self.sound_list))
    
    def _load_option_file(self, filepath, filename):
        """
        Reads the file and returns it in json format.

        Args:
            filename : File name to read. If not, use the file name in the configuration file.

        Returns:
            jsonstr : json format data of the contents of the file

        Raises:

        """
        try:
            fullpath = filepath + filename

            with open(fullpath, "r") as f:
                jsonstr = json.load(f)
        except Exception as e:
            print(str(e))
            return None

        return jsonstr

    def get_sound_option(self, topic_name):  
        return list(filter(lambda sl: sl.topic == topic_name, self.sound_list))
    
    def get_code_list(self):            
        return self.code_list
      
    def get_sound_list(self):            
        return self.sound_list



