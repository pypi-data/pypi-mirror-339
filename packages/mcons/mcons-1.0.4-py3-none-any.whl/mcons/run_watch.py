
import sys
import argparse
from os import path
from watchact import watch_dir_cmds

from .run_build import add_build_argv

def get_build_cmd(pyfile, args: argparse.Namespace):
  argv = "-j" + args.jobs if args.jobs else ""
  return f"{sys.executable} {pyfile} build " + argv
  
def watch(pyfile, cmds):
  src_dir = path.dirname(pyfile)
  build_dir = path.curdir
  watch_dir_cmds(src_dir, 1, cmds, [build_dir], run_now=True)

def run_watch(pyfile):
  def f(args: argparse.Namespace):
    cmds = [] if args.R == None else args.R
    build_cmd = get_build_cmd(pyfile, args)
    watch(pyfile, [build_cmd] + cmds)
  return f

def reg_watch_mode(subparsers, pyfile):
  func = run_watch(pyfile)
  watch_parser = subparsers.add_parser("watch", help="watch mode")
  add_build_argv(watch_parser)
  watch_parser.add_argument("-R", action='append', metavar="command", help="run command")
  watch_parser.set_defaults(func=func)