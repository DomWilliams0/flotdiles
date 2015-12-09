import os

from core import fsutils
from core.flotdile import Flotdiles

flotdiles = Flotdiles()
should_save = True


def handle_command(kwargs):
    cmd = kwargs.pop('subcommand')

    try:

        if cmd == 'add':
            handle_add_remove(kwargs, True)
        elif cmd == "remove":
            handle_add_remove(kwargs, False)
        elif cmd == "list":
            handle_list(kwargs)
        elif cmd == 'sync':
            handle_sync(kwargs)
        elif cmd == 'verify':
            handle_verify(kwargs)
        else:
            raise CommandError("Unknown command '%s'" % cmd)

        if should_save:
            flotdiles.save()

    except CommandError as e:
        print("UH OH: " + e.message)


def handle_add_remove(kwargs, is_add):
    files = kwargs.pop('files')
    all_files = []
    map(lambda f: all_files.extend(fsutils.get_all_files(f)), files)
    all_files = map(lambda f: os.path.expanduser(os.path.expandvars(f)), all_files)

    action = "add" if is_add else "remove"
    func = flotdiles.add_flotdile if is_add else flotdiles.remove_flotdile

    print("Attempting to %s %d file(s)" % (action, len(all_files)))

    map(func, all_files)


def handle_list(kwargs):
    files = flotdiles.get_synced_files()

    if not files:
        print("There are no synced files")
        return

    print("Showing %d synced files: " % len(files))

    print(":-------")
    for src, loc in files.items():
        print(": SRC -> %s" % src)
        print(": LOC -> %s" % loc)
        print(":-------")


def handle_sync(kwargs):
    push = kwargs.get('push', False)
    pull = kwargs.get('pull', False)
    force = kwargs['force']

    # validate
    if push == pull:
        if not push:
            # todo pretty argument error catching
            raise CommandError("You must specify if you want to push or pull with --push or --pull")
        else:
            raise CommandError("Push OR pull, not both!")

    # no git repo
    if not fsutils.is_git_repo(flotdiles.path):
        raise CommandError("flotdiles directory is not a git repository")

    print("Attempting to %s%s" % ("push" if push else "pull", " forcefully" if force else ""))

    func = fsutils.push if push else fsutils.pull
    func(flotdiles.path, force)

    if pull:
        global should_save
        should_save = False

        flotdiles.verify()


def handle_verify(kwargs):
    print("Verifying flotdiles")
    flotdiles.verify()


class CommandError(RuntimeError):
    pass
