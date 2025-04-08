
import yaml
import atexit
import threading
from os import fstat

def read_yaml(filename):
  try:
    with open(filename, 'r', encoding='utf-8') as f:
      mtime = fstat(f.fileno()).st_mtime
      return (mtime, yaml.safe_load(f))
  except:
    return (0, {})

def save_yaml(filename, dict1):
  def f():
    with open(filename, 'w', encoding='utf-8') as f:
      yaml.dump(dict1, f)
  return f

class RecordDict:
  def __init__(self, filename):
    self.lock = threading.Lock()
    self.mtime, self.dict1 = read_yaml(filename)
    atexit.register(save_yaml(filename, self.dict1))

  def get(self, target, target_mtime):
    if self.mtime < target_mtime: 
      return None
    else:
      with self.lock:
        return self.dict1.get(target)
  
  def update(self, target, value):
    with self.lock:
      self.dict1[target] = value
