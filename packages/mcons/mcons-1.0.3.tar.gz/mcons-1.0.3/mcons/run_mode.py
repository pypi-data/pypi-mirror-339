
import argparse

def make_parser(reg_modes):
  parser = argparse.ArgumentParser()
  subparsers = parser.add_subparsers()
  reg_modes(subparsers)
  return parser

def parse_args(parser, argv=None):
  args = parser.parse_args(argv)
  if hasattr(args, 'func'):
    return args
  else:
    parser.print_help()
    exit(0)

def run_cons(reg_modes, argv=None):
  parser = make_parser(reg_modes)
  args = parse_args(parser, argv)
  return args.func(args)
