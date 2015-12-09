#!/usr/bin/env python2

import argparse
import sys

import core


class FlotdileParser(argparse.ArgumentParser):
    def error(self, message):
        sys.stderr.write('error: %s\n' % message)
        self.print_help()
        sys.exit(2)


def main():
    parser = FlotdileParser(description="flotdiles: A dotfile and not-quite-dotfile management system")
    subparsers = parser.add_subparsers(dest="subcommand")

    add = subparsers.add_parser("add", help="Add files and directories")
    add.add_argument("files", nargs="+", help="The files/directories to add")

    rem = subparsers.add_parser("remove", help="Remove files and directories")
    rem.add_argument("files", nargs="*", help="The files/directories to remove")
    rem.add_argument("-A", "--all", help="Remove ALL files", action='store_true', dest='all')

    list = subparsers.add_parser("list", help="List the synced files")

    sync = subparsers.add_parser("sync", help="Sync with the repository")
    sync.add_argument("--push", help="Push change to repository", action='store_true', default=argparse.SUPPRESS)
    sync.add_argument("--pull", help="Pull changes to repository", action='store_true', default=argparse.SUPPRESS)
    sync.add_argument("-f", "--force", help="Force sync, you savage", action='store_true', default=False)

    verify = subparsers.add_parser("verify", help="Verify all flotdiles and remove invalid links")

    args = parser.parse_args()

    core.commands.handle_command(vars(args))


if __name__ == "__main__":
    main()
