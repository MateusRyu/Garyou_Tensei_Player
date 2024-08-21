import tomllib
import os.path

def load_config():
    config_paths = ["~/.config/gtp/config.toml", "/etc/gtp/config.toml", "./config.toml"]
    if os.path.isfile(config_paths[0]):
        path = 0
    elif os.path.isfile(config_paths[1]):
        path = 1
    else:
        path = 2

    with open(config_paths[path], "rb") as file:
        data = tomllib.load(file)
        return data
