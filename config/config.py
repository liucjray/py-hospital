import os
import configparser


def get_config():
    cfg = configparser.ConfigParser(interpolation=configparser.BasicInterpolation())
    cfg_path = (os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.ini"))
    cfg.read(cfg_path)
    return cfg
