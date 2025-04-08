
import subprocess
import threading
from os import path

def memo(func):
  has_eval = False
  value = None
  lock = threading.Lock()
  def f():
    nonlocal has_eval, value
    with lock:
      if not has_eval:
        value = func()
        has_eval = True
      return value
  return f

def replace_ext(filename, new_extension):
  name, ext = path.splitext(filename)
  return name + new_extension

def run_command(cwd, line, check=True):
  try:
    subprocess.run(line.split(), cwd=cwd, check=check)
  except:
    exit(1)
