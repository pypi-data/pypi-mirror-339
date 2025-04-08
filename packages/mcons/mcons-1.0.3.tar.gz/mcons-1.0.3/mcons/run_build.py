
import argparse
from threading import Lock

from .rule import TravelStatus
from .env import batch_map, env
from .config import read_config
from .cons_module import Rule, SourceRule, TargetRule

def add_build_argv(build_parser):
  build_parser.add_argument("-j", "--jobs", metavar="N", help="allow N jobs")
  build_parser.add_argument("-p", "--print-command", action='store_true', help="print command")
  build_parser.add_argument("-q", "--quiet", action='store_true', help="don't print message")

def parse_jobs(jobs):
  if jobs == None:
    return None
  try:
    return int(jobs)
  except:
    print("jobs option error:", jobs)
    exit(1)

def travel_rule(rule, status, default_ret, func):
  if isinstance(rule, TargetRule):
    with rule.lock:
      if rule.travel_status == status:
        return default_ret
      else:
        rule.travel_status = status
        return func(rule)
  else:
    return default_ret

def count1(rule: TargetRule):
  invalids = batch_map(count, rule.deps)
  valid = rule.check_func()
  s = 0 if valid else 1
  return s + sum(invalids)

def count(rule: Rule):
  return travel_rule(rule, TravelStatus.HasCount, 0, count1)

def build(root_rule: Rule, invalid_num, print_command, quiet):
  rank = 0
  lock = Lock()
  def print_message(rule):
    nonlocal rank
    if quiet: return
    with lock:
      progress = f"[{rank}/{invalid_num}] "
      print(progress + rule.get_message(print_command))
      rank = rank + 1

  def build0(rule: TargetRule):
    batch_map(build1, rule.deps)
    if not rule.valid:
      print_message(rule)
      rule.build_func()
      return rule

  def build1(rule: Rule):
    return travel_rule(rule, TravelStatus.HasBuild, rule, build0)

  build1(root_rule)
  print("finish")

def run_build(cons):
  def f(args: argparse.Namespace):
    read_config()
    thread_num = parse_jobs(args.jobs)
    env.init_build(thread_num)
    rule = cons()
    invalid_num = count(rule)
    build(rule, invalid_num, args.print_command, args.quiet)
  return f

def reg_build_mode(subparsers, cons):
  func = run_build(cons)
  build_parser = subparsers.add_parser("build", help="build project")
  add_build_argv(build_parser)
  build_parser.set_defaults(func=func)