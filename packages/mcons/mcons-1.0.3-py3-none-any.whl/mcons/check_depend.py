
from typing import Iterable

from .cons_module import Rule
from .env import env

def compare_depends_mtime(target: Rule, deps: Iterable[Rule]):
  for dep in deps:
    if not dep.valid:
      return True
    elif target.mtime < dep.mtime:
      return True
  return False

def check_mark(target: Rule, mark):
  if target.valid:
    mark0 = env.mark_dict.get(target.filepath, target.mtime)
    if mark0 == mark: return False

  env.mark_dict.update(target.filepath, mark)
  return True

def need_update(target: Rule, deps: Iterable[Rule], mark=""):
  if check_mark(target, mark):
    return True
  else:
    return compare_depends_mtime(target, deps)
