
from os import remove

from .config import read_config
from .env import env
from .rule import Rule, TargetRule
from .env import batch_map, env

def remove_file(filepath):
  try:
    remove(filepath)
    print("clean", filepath)
  except:
    None

def clean(rule: Rule):
  if isinstance(rule, TargetRule):
    remove_file(rule.filepath)
    batch_map(clean, rule.deps)

def run_clean(cons, extra_files):
  def f(args):
    remove_file(env.mark_dict_filename)
    remove_file(env.header_depend_filename)
    remove_file(env.compile_commands_filename)

    for name in extra_files:
      remove_file(name)

    read_config()
    env.init_clean(None)
    clean(cons())
  return f

def reg_clean_mode(subparsers, cons, extra_files=[]):
  watch_parser = subparsers.add_parser("clean", help="clean mode")
  watch_parser.set_defaults(func=run_clean(cons, extra_files))
