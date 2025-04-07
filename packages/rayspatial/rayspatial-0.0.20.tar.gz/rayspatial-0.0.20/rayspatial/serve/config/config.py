import configparser
import os

class Config:
    config_ray = None
    config_redis = None
    config_base = None


    def __init__(self):
        self.config = configparser.ConfigParser()
        current_dir = os.path.abspath(os.path.dirname(__file__))
        default_config = os.path.join(current_dir, 'config.ini')
        self.config.read(default_config)
        self.config_ray = self.config['ray']
        self.config_redis = self.config['redis']
        self.config_base = self.config['base']
        

class EngineConfig:
    ray_address_ip = None
    ray_address_port = None
    scale = None
    logging_level = "INFO"


config = Config()

engine_config = EngineConfig()
