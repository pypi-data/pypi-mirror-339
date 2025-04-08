
import sys

from .record_dict import read_yaml, save_yaml
from .env import env

def get_config():
  return env.config

def config_format(templ):
  return templ.format(**env.config)

def read_config():
  try:
    config_mtime, config_content = read_yaml(env.config_filename)
    if config_content["mcons_version"] != "1.0.2":
      print("mcons_config.yaml version mismatch, please run")
      print(sys.argv[0] + " init")
      exit(1)
    else:
      env.config = config_content["config"]
  except:
    print("mcons_config.yaml not found, please run")
    print(sys.argv[0] + " init")
    exit(1)

def save_config():
  config_content = {"mcons_version": "1.0.2", "config": env.config}
  save_yaml(env.config_filename, config_content)()
