
from typing import Iterable

from .rule import TargetRule
from .cons_module import ConsModule, Rule
from .env import batch, batch_map, env
from .check_depend import need_update
from .utils import replace_ext, run_command
from .object_rule import object_rule

def cons_object_list(cm: ConsModule, sources: Iterable[str], ext: str, compile_templ: str):
  def f(src):
    return object_rule(cm, src, replace_ext(src, ext), compile_templ)
  return batch_map(f, sources)

def pack_ar(cm: ConsModule, name: str, sources: Iterable[str], compile_templ: str):
  objects = cons_object_list(cm, sources, ".o", compile_templ)
  cmd = "ar rcs {1} {0}"
  return task(cm, name, objects, cmd)

def task(cm: ConsModule, name: str, deps: Iterable[Rule], templ: str):
  target = cm.target(name, deps, None, None)
  deps1 = ' '.join(map(str, deps))
  cmd = templ.format(deps1, target, **env.config)
  cwd = cm.build_dir

  def check_func():
    valid = not need_update(target, deps, cmd)
    target.valid = valid
    return valid

  def build_func():
    run_command(cwd, cmd)
    target.update()
  
  def get_message(verbose):
    color_filepath = f"\033[32;1m{target.filepath}\033[0m"
    if not verbose:
      return color_filepath
    else:
      return '\n'.join([color_filepath, cwd, cmd])

  target.check_func = check_func
  target.build_func = build_func
  target.get_message = get_message
  return target

def rule(cm: ConsModule, name: str, deps: Iterable[Rule], func, mark=""):
  target = cm.target(name, deps, None, None)

  def check_func():
    valid = not need_update(target, deps, mark)
    target.valid = valid
    return valid

  def build_func():
    func()
    target.update()
  target.check_func = check_func
  target.build_func = build_func
  target.get_message = lambda verbose: f"\033[32;1m{target.filepath}\033[0m"
  return target

def phony_target(name: str, deps: Iterable[Rule], func=lambda: None):
  target = TargetRule(name, deps, None, func)

  def check_func():
    target.valid = False
    return False

  target.check_func = check_func
  target.get_message = lambda verbose: f"\033[32;1m{target.filepath}\033[0m"
  return target