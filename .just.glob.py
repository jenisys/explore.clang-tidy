#!/usr/bin/env python3
"""
JUST HELPER FUNCTION: Performs filename-wildcard globbing.
Supports ANT-like patterns, like: "**/*.cpp"
"""

import os
import sys
from pathlib import Path


DEBUG = os.environ.get("DEBUG", "OFF") in ("ON", "1")


def path_glob(pattern):
    return [str(p) for p in Path(".").glob(pattern)]


def print_glob_diag(args, pattern, paths):
    print("DIAG: ____________________" )
    print("  CWD: %s" % Path.cwd())
    print("  args[%d]: %r;" % (len(args), args))
    print("  pattern: %s;" % pattern)
    print("  paths[%d]: %s" % (len(paths), "\n    ".join(paths)))


def main_glob(args=None):
    args = args or sys.argv[1:]
    if not args:
        name = Path(__file__).name
        print("USAGE: {0} FILE_PATTERN".format(name))
        sys.exit(1)

    pattern = args[0]
    paths = path_glob(pattern)
    print(" ".join(paths))
    if DEBUG:
        print_glob_diag(args, pattern=pattern, paths=paths)


if __name__ == "__main__":
    sys.exit(main_glob())
