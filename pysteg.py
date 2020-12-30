#!/usr/bin/python
"""pysteg.py

Main entry point for pysteg. Provides a command line interface.
"""


import argparse
import importlib
import os
import os.path
import sys
import unittest


__PROJECT_DIR = os.path.abspath(os.path.join(__file__, ".."))


def workload_test(args):
    """Run specified test workloads.

    Parameters:
        args    Parsed command line arguments

    Return:
        None.
    """
    test_prefix = "test_"
    test_postfix = ".py"

    modules = []
    for root, dirs, files in os.walk("tests"):
        for f in files:
            if f.startswith(test_prefix) and f.endswith(test_postfix):
                root_module = ".".join(os.path.split(root))
                module = f"{root_module}.{f.rstrip('.py')}"
                modules.append(module)

    for module in modules:
        imported = importlib.import_module(module)
        suite = unittest.TestLoader().loadTestsFromModule(imported)
        unittest.TextTestRunner().run(suite)


def argument_setup():
    """Set up the command line argument parser.

    Parameters:
        None

    Returns:
        The parsed arguments.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--type", type=str,
                        help="File type")
    parser.add_argument("--test", action="store_true", default=False,
                        help="Run validation and/or verification tests")

    return parser.parse_args()


def main():
    args = argument_setup()

    if args.test:
        workload_test(args)


if __name__ == "__main__":
    root_dir = os.path.abspath(os.path.join(__PROJECT_DIR, ".."))
    if root_dir not in sys.path:
        sys.path.append(root_dir)

    main()
