import argparse


def main():
    parser = argparse.ArgumentParser(description="flotdiles")
    subparsers = parser.add_subparsers(dest="subcommand")

    add = subparsers.add_parser("add", help="Add files and directories")
    add.add_argument("files", nargs="+", help="The files/directories to add")

    rem = subparsers.add_parser("remove", help="Remove files and directories")
    rem.add_argument("files", nargs="+", help="The files/directories to remove")

    list = subparsers.add_parser("list", help="List the synced files")

    sync = subparsers.add_parser("sync", help="Sync with the repository")
    sync.add_argument("-p", "--push", help="Push change to repository", action='store_true')
    sync.add_argument("-P", "--pull", help="Pull changes to repository", action='store_true')
    sync.add_argument("-f", "--force", help="Force sync, you savage", action='store_true')

    args = parser.parse_args()
    print args


if __name__ == "__main__":
    main()
