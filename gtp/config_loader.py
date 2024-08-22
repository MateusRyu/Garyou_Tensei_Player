import tomllib
import os.path

def get_configs_path():
    app_folder = os.path.dirname(os.path.realpath(__file__))
    config_folder = app_folder.split("/")
    config_folder[-1] = "configs"
    config_folder = "/".join(config_folder)
    return config_folder

def load_config():
    config_folder = get_configs_path()
    config_paths = ["~/.config/gtp/config.toml", "/etc/gtp/config.toml", f"{config_folder}/config.toml"]
    if os.path.isfile(config_paths[0]):
        path = 0
    elif os.path.isfile(config_paths[1]):
        path = 1
    else:
        path = 2

    with open(config_paths[path], "rb") as file:
        data = tomllib.load(file)
        return data
