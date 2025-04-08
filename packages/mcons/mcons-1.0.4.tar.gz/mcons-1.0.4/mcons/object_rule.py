
import subprocess
import tempfile

from .cons_module import ConsModule, Rule
from .check_depend import check_mark, compare_depends_mtime
from .utils import run_command
from .env import env

def parse_depfile(depfile):
  depfile.seek(0)
  content = depfile.read()
  r = content.split()
  return list(filter(lambda x: x != '\\', r[1:]))

def update_depend(cm: ConsModule, target: Rule, line: str):
  cwd = cm.build_dir
  try:
    with tempfile.NamedTemporaryFile(mode='w+') as depfile:
      line1 = line + f" -MM -MF {depfile.name}"
      subprocess.run(line1.split(), cwd=cwd, check=True, stdout=subprocess.DEVNULL)
      deps = parse_depfile(depfile)
      env.header_depend.update(target.filepath, deps)
      return deps
  except:
    print("update_depend error:", cwd, ":", line)
    exit(1)

def get_depends(cm: ConsModule, target: Rule, line: str):
  if target.valid:
    deps = env.header_depend.get(target.filepath, target.mtime)
    if deps: return deps
  return update_depend(cm, target, line)

def object_need_update(cm: ConsModule, target: Rule, line: str):
  if check_mark(target, line):
    return True
  else:
    deps = get_depends(cm, target, line)
    deps1 = map(cm.src, deps)
    return compare_depends_mtime(target, deps1)

def object_rule(cm: ConsModule, src: str, obj: str, compile_templ: str):
  src1 = cm.src(src)
  target = cm.target(obj, [src1], None, None)
  line = compile_templ.format(src1, target, **env.config)
  cwd = cm.build_dir

  def check_func():
    env.compile_commands.push(cwd, src1.filepath, line)
    valid = not object_need_update(cm, target, line)
    target.valid = valid
    return valid

  def build_func():
    update_depend(cm, target, line)
    run_command(cwd, line)
    target.update()

  def get_message(verbose):
    color_filepath = f"\033[32m{target}\033[0m"
    if not verbose:
      return color_filepath
    else:
      return '\n'.join([color_filepath, cwd, line])

  target.check_func = check_func
  target.build_func = build_func
  target.get_message = get_message
  return target
