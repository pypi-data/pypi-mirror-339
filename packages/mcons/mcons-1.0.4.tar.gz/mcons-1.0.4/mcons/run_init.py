
import argparse

from .env import env
from .config import save_config

def put_defs(config, D):
  defs = [] if D == None else D
  for pair in defs:
    p = pair.split("=", 1)
    value = True if len(p) == 1 else p[1]
    config[p[0]] = value

def run_init(put_config, default_config):
  def f(args: argparse.Namespace):
    config = default_config
    put_defs(config, args.D)
    put_config(config)
    env.config = config
    save_config()
  return f

def empty_put_config(config):
  None

def reg_init_mode(subparsers, put_config=empty_put_config, default_config={}):
  func = run_init(put_config, default_config)
  init_parser = subparsers.add_parser("init", help="init args")
  init_parser.add_argument("-D", action='append', metavar="KEY[=VALUE]", help="define key value pair")
  init_parser.set_defaults(func=func)