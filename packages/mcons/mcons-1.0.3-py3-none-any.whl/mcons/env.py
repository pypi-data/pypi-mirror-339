
from .record_dict import RecordDict
from .thread_pool import ThreadPool
from .compile_commands import CompileCommands

class Env:
  def __init__(self):
    self.config = {}
    self.config_filename = "mcons_config.yaml"
    self.mark_dict_filename = "mark_dict.yaml"
    self.header_depend_filename = "header_depend.yaml"
    self.compile_commands_filename = "compile_commands.json"

  def init_build(self, thread_num):
    self.mark_dict = RecordDict(self.mark_dict_filename)
    self.header_depend = RecordDict(self.header_depend_filename)
    self.compile_commands = CompileCommands(self.compile_commands_filename)
    self.thread_pool = ThreadPool(thread_num)

  def init_clean(self, thread_num):
    self.thread_pool = ThreadPool(thread_num)

env = Env()

def batch(tasks):
  return env.thread_pool.batch(tasks)

def batch_map(f, xs):
  f1 = lambda x: lambda: f(x)
  tasks = map(f1, xs)
  return batch(tasks)