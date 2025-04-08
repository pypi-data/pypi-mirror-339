
import json
import atexit
import threading

def read_json(filename):
  try:
    with open(filename, 'r', encoding='utf-8') as file:
      commands_dict = {}
      for item in json.load(file):
        commands_dict[item["file"]] = item
      return commands_dict
  except:
    return {}

def update_json(filename, dict1):
  def f():
    dict0 = read_json(filename)
    dict0.update(dict1)
    commands = list(dict0.values())
    with open(filename, 'w', encoding='utf-8') as file:
      json.dump(commands, file, indent=4)
  return f

class CompileCommands:
  def __init__(self, filename):
    self.lock = threading.Lock()
    self.commands_dict = {}
    atexit.register(update_json(filename, self.commands_dict))

  def push(self, cwd: str, file: str, command: str):
    with self.lock:
      item = {"directory": cwd, "file": file, "command": command}
      self.commands_dict[file] = item
