import os
import json

script_dir = os.path.dirname(os.path.realpath(__file__))
config_path = os.path.join(script_dir, "config.json")

with open(config_path, "r") as config_file:
    config = json.load(config_file)

def set_custom_config(custom_config_path):
    with open(custom_config_path, "r") as custom_config_file:
        custom_config = json.load(custom_config_file)
        config.update(custom_config)